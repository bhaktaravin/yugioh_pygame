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
    print("Starting Yu-Gi-Oh! Duelist of the Roses")
    print("="*50)
    
    # Start the game directly
    game = Game()
    game.run()

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