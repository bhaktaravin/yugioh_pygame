#!/usr/bin/env python3
"""
Quick test to upload a few cards from Excel to Supabase
"""
from listofcards.getting_all_cards import grab_worksheet_of_monsters
from background.api_client import YugiohAPIClient
from database.db import upload_card_to_supabase
import tempfile
import os
import requests

# Load first 5 monster cards
monsters = grab_worksheet_of_monsters('DuelistofTheRoses.xlsx', 'assets/excelspreadsheet')
api_client = YugiohAPIClient()

print(f"\n📤 Testing upload of first 5 monsters...")
print("="*60)

for idx in range(min(5, len(monsters))):
    row = monsters.iloc[idx]
    card_name = str(row.get('Name ', '')).strip()
    
    if not card_name:
        continue
    
    print(f"\n[{idx+1}/5] Processing: {card_name}")
    
    # Fetch from API
    card_data = api_client.fetch_card_by_name(card_name)
    
    if card_data and 'card_images' in card_data:
        image_url = card_data['card_images'][0].get('image_url')
        print(f"  ✓ Found in API: {image_url}")
        
        if image_url:
            try:
                # Download to temp file
                response = requests.get(image_url)
                if response.status_code == 200:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                        tmp.write(response.content)
                        tmp_path = tmp.name
                    
                    print(f"  ✓ Downloaded to temp file")
                    
                    # Upload to Supabase
                    supabase_url = upload_card_to_supabase(tmp_path, card_name, 'Monster')
                    
                    # Clean up
                    os.unlink(tmp_path)
                    
                    if supabase_url:
                        print(f"  ✅ Uploaded to: {supabase_url}")
                    else:
                        print(f"  ❌ Upload failed")
                else:
                    print(f"  ❌ Download failed: {response.status_code}")
            except Exception as e:
                print(f"  ❌ Error: {e}")
        else:
            print(f"  ❌ No image URL")
    else:
        print(f"  ❌ Not found in API")

print("\n" + "="*60)
print("Test complete!")
