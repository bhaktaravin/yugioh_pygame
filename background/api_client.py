"""
Yu-Gi-Oh! API Client
Fetches card information from the official YGOPRODeck API
https://ygoprodeck.com/api-guide/
"""
import requests
import os
from pathlib import Path


class YugiohAPIClient:
    BASE_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    
    def __init__(self, image_dir="assets"):
        self.image_dir = Path(image_dir)
        self.session = requests.Session()
        
    def fetch_all_cards(self):
        """Fetch all Yu-Gi-Oh cards from the API"""
        try:
            print("Fetching all cards from YGOPRODeck API...")
            response = self.session.get(self.BASE_URL)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data:
                print(f"✅ Retrieved {len(data['data'])} cards")
                return data['data']
            return []
        except requests.RequestException as e:
            print(f"❌ Error fetching cards: {e}")
            return []
    
    def fetch_card_by_name(self, name):
        """Fetch a specific card by name"""
        try:
            params = {'name': name}
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                return data['data'][0]
            return None
        except requests.RequestException as e:
            print(f"❌ Error fetching card '{name}': {e}")
            return None
    
    def download_card_image(self, card_data, card_type='monsters'):
        """
        Download card image from API data
        
        Args:
            card_data: Card data from API
            card_type: 'monsters', 'spells', or 'traps'
        
        Returns:
            Path to downloaded image or None
        """
        try:
            name = card_data.get('name', 'unknown')
            card_images = card_data.get('card_images', [])
            
            if not card_images:
                print(f"No images available for {name}")
                return None
            
            # Get the first image URL (usually the main card image)
            image_url = card_images[0].get('image_url')
            if not image_url:
                print(f"No image URL for {name}")
                return None
            
            # Create directory structure
            card_dir = self.image_dir / card_type
            card_dir.mkdir(parents=True, exist_ok=True)
            
            # Clean filename
            clean_name = self._clean_filename(name)
            image_path = card_dir / f"{clean_name}.jpg"
            
            # Download image
            print(f"Downloading: {name}...")
            img_response = self.session.get(image_url, stream=True)
            img_response.raise_for_status()
            
            with open(image_path, 'wb') as f:
                for chunk in img_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Saved: {image_path}")
            return str(image_path)
            
        except Exception as e:
            print(f"❌ Error downloading image for {card_data.get('name', 'unknown')}: {e}")
            return None
    
    def download_cards_by_type(self, card_type='Monster', limit=None):
        """
        Download cards of a specific type
        
        Args:
            card_type: 'Monster', 'Spell Card', or 'Trap Card'
            limit: Maximum number of cards to download (None for all)
        
        Returns:
            List of (name, image_path) tuples
        """
        cards = self.fetch_all_cards()
        if not cards:
            return []
        
        # Filter by type
        filtered_cards = [c for c in cards if c.get('type') == card_type or 
                         (card_type == 'Spell Card' and 'Spell' in c.get('type', '')) or
                         (card_type == 'Trap Card' and 'Trap' in c.get('type', ''))]
        
        if limit:
            filtered_cards = filtered_cards[:limit]
        
        print(f"\nFound {len(filtered_cards)} {card_type} cards")
        
        # Determine folder
        folder_map = {
            'Monster': 'monsters',
            'Spell Card': 'spells',
            'Trap Card': 'traps'
        }
        folder = folder_map.get(card_type, 'monsters')
        
        # Download images
        results = []
        for i, card in enumerate(filtered_cards, 1):
            name = card.get('name')
            print(f"[{i}/{len(filtered_cards)}] ", end="")
            image_path = self.download_card_image(card, folder)
            if image_path:
                results.append((name, image_path))
        
        return results
    
    def get_card_info(self, card_data):
        """Extract just title and image URL from card data"""
        return {
            'name': card_data.get('name'),
            'image_url': card_data.get('card_images', [{}])[0].get('image_url'),
            'type': card_data.get('type')
        }
    
    @staticmethod
    def _clean_filename(name):
        """Clean card name for use as filename"""
        # Remove invalid filename characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '')
        return name.strip()


def download_sample_cards():
    """Download a sample set of popular cards"""
    client = YugiohAPIClient()
    
    popular_cards = [
        'Dark Magician',
        'Blue-Eyes White Dragon',
        'Red-Eyes Black Dragon',
        'Exodia the Forbidden One',
        'Dark Hole',
        'Mirror Force',
        'Pot of Greed',
        'Raigeki'
    ]
    
    print("Downloading popular Yu-Gi-Oh! cards...\n")
    
    for card_name in popular_cards:
        card_data = client.fetch_card_by_name(card_name)
        if card_data:
            card_type = card_data.get('type', '')
            if 'Monster' in card_type:
                folder = 'monsters'
            elif 'Spell' in card_type:
                folder = 'spells'
            elif 'Trap' in card_type:
                folder = 'traps'
            else:
                folder = 'monsters'
            
            client.download_card_image(card_data, folder)
    
    print("\n✅ Sample cards downloaded!")


if __name__ == "__main__":
    # Test the API client
    client = YugiohAPIClient()
    
    # Download sample cards
    download_sample_cards()
    
    # Or download specific types
    # client.download_cards_by_type('Monster', limit=10)
    # client.download_cards_by_type('Spell Card', limit=5)
    # client.download_cards_by_type('Trap Card', limit=5)
