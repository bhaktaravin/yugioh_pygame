#!/usr/bin/env python3
"""
Download cards from YGOPRODeck API
Usage: python download_cards.py
"""
from background.api_client import YugiohAPIClient, download_sample_cards


def main():
    print("Yu-Gi-Oh! Card Downloader")
    print("="*50)
    print("\nOptions:")
    print("1. Download sample popular cards (8 cards)")
    print("2. Download specific card by name")
    print("3. Download all monsters (WARNING: Large download)")
    print("4. Download all spells (WARNING: Large download)")
    print("5. Download all traps (WARNING: Large download)")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    client = YugiohAPIClient()
    
    if choice == "1":
        download_sample_cards()
    
    elif choice == "2":
        card_name = input("Enter card name: ").strip()
        card_data = client.fetch_card_by_name(card_name)
        if card_data:
            info = client.get_card_info(card_data)
            print(f"\n✅ Found: {info['name']}")
            print(f"   Type: {info['type']}")
            print(f"   Image: {info['image_url']}")
            
            # Determine folder
            card_type = info['type']
            if 'Monster' in card_type:
                folder = 'monsters'
            elif 'Spell' in card_type:
                folder = 'spells'
            elif 'Trap' in card_type:
                folder = 'traps'
            else:
                folder = 'monsters'
            
            client.download_card_image(card_data, folder)
        else:
            print(f"❌ Card '{card_name}' not found")
    
    elif choice == "3":
        limit = input("How many monsters? (or 'all'): ").strip()
        limit = None if limit.lower() == 'all' else int(limit)
        client.download_cards_by_type('Monster', limit=limit)
    
    elif choice == "4":
        limit = input("How many spells? (or 'all'): ").strip()
        limit = None if limit.lower() == 'all' else int(limit)
        client.download_cards_by_type('Spell Card', limit=limit)
    
    elif choice == "5":
        limit = input("How many traps? (or 'all'): ").strip()
        limit = None if limit.lower() == 'all' else int(limit)
        client.download_cards_by_type('Trap Card', limit=limit)
    
    else:
        print("Invalid choice")
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
