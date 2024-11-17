import sys
import os 
from menu.game import Game
from background.downloader import GettingImages


def main(): 
    game = Game() 
    game.run()
    downloader()

####################################  GETTING IMAGES FROM WIKIPEDIA  ####################

def downloader(): 
        print("Downloading images...")

        GettingImages.download_card_images()
        print("Download complete.")

##########################################################################################

if __name__ == "__main__": 
    main() 