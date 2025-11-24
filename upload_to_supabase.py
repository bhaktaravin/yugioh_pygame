#!/usr/bin/env python3
"""
Upload local card images to Supabase storage
This will sync all your local card images to Supabase for cloud access
"""
import os
from database.db import upload_card_to_supabase


def upload_all_cards():
    """Upload all cards from local assets folders to Supabase"""
    
    card_folders = {
        'assets/monsters/': 'Monster',
        'assets/spells/': 'Spell Card',
        'assets/traps/': 'Trap Card'
    }
    
    total_uploaded = 0
    
    for folder_path, card_type in card_folders.items():
        if not os.path.exists(folder_path):
            print(f"⚠️  Folder {folder_path} doesn't exist, skipping...")
            continue
        
        files = [f for f in os.listdir(folder_path) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not files:
            print(f"⚠️  No images in {folder_path}, skipping...")
            continue
        
        print(f"\n📤 Uploading {len(files)} {card_type} cards...")
        
        for i, filename in enumerate(files, 1):
            card_name = os.path.splitext(filename)[0]
            local_path = os.path.join(folder_path, filename)
            
            print(f"  [{i}/{len(files)}] {card_name}...", end=" ")
            
            url = upload_card_to_supabase(local_path, card_name, card_type)
            if url:
                total_uploaded += 1
    
    print(f"\n\n✅ Upload complete! {total_uploaded} cards uploaded to Supabase")
    print("Your cards are now available in the cloud!")


if __name__ == "__main__":
    print("🚀 Supabase Card Uploader")
    print("="*50)
    print("\nThis will upload all local card images to Supabase storage.")
    print("Existing files will be overwritten.\n")
    
    confirm = input("Continue? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        upload_all_cards()
    else:
        print("Upload cancelled.")
