#!/usr/bin/env python3
"""
Load cards from Excel and upload to Supabase with images from YGOPRODeck API
"""
import pandas as pd
from listofcards.getting_all_cards import grab_worksheet_of_monsters, grab_worksheet_of_spells, grab_worksheet_of_traps
from background.api_client import YugiohAPIClient
from database.db import upload_card_to_supabase
import os
import tempfile


def download_and_upload_cards_from_excel():
    """
    Load cards from Excel, download images from API, upload to Supabase
    """
    filename = "DuelistofTheRoses.xlsx"
    search_path = "assets/excelspreadsheet"
    
    # Initialize API client
    api_client = YugiohAPIClient()
    
    print("🎴 Loading card data from Excel...")
    print("="*60)
    
    # Load all card types
    monsters = grab_worksheet_of_monsters(filename, search_path)
    spells = grab_worksheet_of_spells(filename, search_path)
    traps = grab_worksheet_of_traps(filename, search_path)
    
    total_uploaded = 0
    
    # Process monsters
    if not monsters.empty:
        print(f"\n📤 Processing {len(monsters)} monster cards...")
        for idx, row in monsters.iterrows():
            # Try different column name variations
            card_name = row.get('Name ', row.get('Name', row.get('name', '')))
            card_name = str(card_name).strip() if card_name else ''
            
            if not card_name or pd.isna(card_name):
                continue
            
            print(f"  [{idx+1}/{len(monsters)}] {card_name}...", end=" ")
            
            # Fetch from API
            card_data = api_client.fetch_card_by_name(card_name)
            if card_data and 'card_images' in card_data:
                image_url = card_data['card_images'][0].get('image_url')
                
                if image_url:
                    # Download to temp file
                    try:
                        import requests
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            # Save to temp file
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                                tmp.write(response.content)
                                tmp_path = tmp.name
                            
                            # Upload to Supabase
                            supabase_url = upload_card_to_supabase(tmp_path, card_name, 'Monster')
                            
                            # Clean up
                            os.unlink(tmp_path)
                            
                            if supabase_url:
                                total_uploaded += 1
                                print("✅")
                            else:
                                print("❌")
                        else:
                            print("❌ Download failed")
                    except Exception as e:
                        print(f"❌ {e}")
                else:
                    print("❌ No image URL")
            else:
                print("❌ Not found in API")
    
    # Process spells
    if not spells.empty:
        print(f"\n📤 Processing {len(spells)} spell cards...")
        for idx, row in spells.iterrows():
            card_name = row.get('Name ', row.get('Name', row.get('name', '')))
            card_name = str(card_name).strip() if card_name else ''
            
            if not card_name or pd.isna(card_name):
                continue
            
            print(f"  [{idx+1}/{len(spells)}] {card_name}...", end=" ")
            
            card_data = api_client.fetch_card_by_name(card_name)
            if card_data and 'card_images' in card_data:
                image_url = card_data['card_images'][0].get('image_url')
                
                if image_url:
                    try:
                        import requests
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                                tmp.write(response.content)
                                tmp_path = tmp.name
                            
                            supabase_url = upload_card_to_supabase(tmp_path, card_name, 'Spell Card')
                            os.unlink(tmp_path)
                            
                            if supabase_url:
                                total_uploaded += 1
                                print("✅")
                            else:
                                print("❌")
                        else:
                            print("❌ Download failed")
                    except Exception as e:
                        print(f"❌ {e}")
                else:
                    print("❌ No image URL")
            else:
                print("❌ Not found in API")
    
    # Process traps
    if not traps.empty:
        print(f"\n📤 Processing {len(traps)} trap cards...")
        for idx, row in traps.iterrows():
            card_name = row.get('Name ', row.get('Name', row.get('name', '')))
            card_name = str(card_name).strip() if card_name else ''
            
            if not card_name or pd.isna(card_name):
                continue
            
            print(f"  [{idx+1}/{len(traps)}] {card_name}...", end=" ")
            
            card_data = api_client.fetch_card_by_name(card_name)
            if card_data and 'card_images' in card_data:
                image_url = card_data['card_images'][0].get('image_url')
                
                if image_url:
                    try:
                        import requests
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                                tmp.write(response.content)
                                tmp_path = tmp.name
                            
                            supabase_url = upload_card_to_supabase(tmp_path, card_name, 'Trap Card')
                            os.unlink(tmp_path)
                            
                            if supabase_url:
                                total_uploaded += 1
                                print("✅")
                            else:
                                print("❌")
                        else:
                            print("❌ Download failed")
                    except Exception as e:
                        print(f"❌ {e}")
                else:
                    print("❌ No image URL")
            else:
                print("❌ Not found in API")
    
    print(f"\n\n{'='*60}")
    print(f"✅ Upload complete! {total_uploaded} cards uploaded to Supabase")
    print(f"   Monsters: {len(monsters)}")
    print(f"   Spells: {len(spells)}")
    print(f"   Traps: {len(traps)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    print("🚀 Excel to Supabase Card Uploader")
    print("="*60)
    print("\nThis will:")
    print("1. Load cards from DuelistofTheRoses.xlsx")
    print("2. Download images from YGOPRODeck API")
    print("3. Upload to Supabase cloud storage")
    print("\nThis may take several minutes depending on card count.\n")
    
    confirm = input("Continue? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        download_and_upload_cards_from_excel()
    else:
        print("Upload cancelled.")
