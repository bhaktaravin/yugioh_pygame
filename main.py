import sys
import os
import requests
import re
from menu.game import Game
from background.downloader import GettingImages

CARD_IMAGE_FOLDER = "card_images"
YGOPRO_API = "https://db.ygoprodeck.com/api/v7/cardinfo.php?"


# Common Yu-Gi-Oh! words that should be separated
KNOWN_WORDS = {"of", "the", "and", "dragon", "magician", "knight", "lord", "dark", "light", "beast", "king", "queen", "guardian"}


def main(): 

    print("Cards have been downloaded... You may start the game.")

    pattern = r"\d+px-(.*?)-DOR-EN-VG"
    cards = {}

    if not os.path.exists(CARD_IMAGE_FOLDER):
        print(f"Error: Folder '{CARD_IMAGE_FOLDER}' not found!")
        return

    # Convert images into objects for better performance
    for file in os.listdir(CARD_IMAGE_FOLDER):
        filename, ext = os.path.splitext(file)
        match = re.search(pattern, filename)

        if match:
            raw_card_name = match.group(1)
            formatted_card_name = format_card_name(raw_card_name)  # Fix spacing
            
            # Create API URL
            url = YGOPRO_API + f"name={formatted_card_name}"
            print(f"API Request URL: {url}")  # Debugging output

            # Try fetching card data from API
            try:
                response = requests.get(url)
                response.raise_for_status()  # Check if request was successful
                card_data = response.json()
                
                if 'data' in card_data:
                    cards[formatted_card_name] = card_data
                    print(f"✅ Card Data Retrieved: {card_data['data'][0]['name']}")
                else:
                    print(f"❌ No data found for '{formatted_card_name}'")

            except requests.RequestException as e:
                print(f"❌ Failed to fetch data for '{formatted_card_name}': {e}")

    print("Cards have been converted into objects... You may start the game.")

    # Start the game
    game = Game()
    # game.run()

####################################  GETTING IMAGES FROM WIKIPEDIA  ####################

def downloader():
    print("Downloading images...")
    
    try:
        #GettingImages.download_card_images()
        image_downloader = GettingImages() 
        image_downloader.download_card_images()

        
        print("Download complete.")
    except Exception as e:
        print(f"❌ Image download failed: {e}")

##########################################################################################

####################################  FORMATTING CARD NAMES  ############################

def format_card_name(raw_name):
    """
    Converts a filename-based card name into a properly formatted one.
    Example: "Maidenofthe Moonlight" -> "Maiden of the Moonlight"
    """
    # Fix PascalCase (e.g., "DarkMagician" → "Dark Magician")
    spaced_name = re.sub(r"([a-z])([A-Z])", r"\1 \2", raw_name)

    # Ensure known words are separated
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z])', spaced_name)
    formatted_words = []

    for word in words:
        if word.lower() in KNOWN_WORDS:
            formatted_words.append(word.lower())  # Keep small words in lowercase
        else:
            formatted_words.append(word)  # Keep other words as they are

    return " ".join(formatted_words).title()  # Convert to title case

#########################################################################################

if __name__ == "__main__":
    main()

    try:
        input("Press Enter to exit...")
    except KeyboardInterrupt:
        pass
