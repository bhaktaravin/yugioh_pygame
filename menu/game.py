import pygame
import pygame_menu
import os
from menu.background.card_manager import CardManager
from listofcards.getting_all_cards import *
from database.db import load_cards_from_file

# Global constants
WIDTH, HEIGHT = 800, 600

# Function to get the full file path
def get_full_path(file_name):
    return os.path.abspath(file_name)

# Initialize Pygame
pygame.init()

# Load images and handle missing files
bg_image_path = get_full_path('assets/background.jpg')
card_back_image_path = get_full_path('assets/card_back.png')

# Print file paths for debugging
print(f"Background image path: {bg_image_path}")
print(f"Card image path: {card_back_image_path}")

try:
    bg_image = pygame.image.load(bg_image_path)
    back_card_image = pygame.image.load(card_back_image_path)
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# Scale the card image to the desired size
back_card_image = pygame.transform.scale(back_card_image, (80, 120))


class Game: 
    def __init__(self): 
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Yu-Gi-Oh! Duel')
        self.card_manager = CardManager(back_card_image)
        self.clock = pygame.time.Clock()
        self.running = True 

        self.flip_card_timer = 0

        # Set up the menu
        self.custom_theme = pygame_menu.themes.THEME_DARK.copy()
        self.custom_theme.background_color = (0, 0, 0, 0)
        self.menu = pygame_menu.Menu('Yu-Gi-Oh! Duel Menu', WIDTH, HEIGHT, theme=self.custom_theme)
        self.menu.add.button('Start Game', self.start_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

################################### START GAME METHOD #################
    def start_game(self):
        
        # Implement the game logic here
        print("Loading the Cards Into the Database")
        
        print("Cards Loaded")
        filename = "DuelistofTheRoses.xlsx"
        search_path = "."
        monsters = grab_worksheet_of_monsters(filename, search_path)

        spells = grab_worksheet_of_spells(filename, search_path)
        traps = grab_worksheet_of_traps(filename, search_path)

        load_cards_from_file(monsters, 'Monster')
        load_cards_from_file(spells, 'Spells')
        load_cards_from_file(traps, 'Traps')
        #print(type(monsters))

######################################################################

################################### RUN METHOD #######################

    def run(self):
        while self.running:
            self.screen.blit(bg_image, (0, 0))
            self.card_manager.update()
            self.card_manager.draw(self.screen)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.menu.is_enabled():
                self.menu.update(events)
                self.menu.draw(self.screen)

            self.flip_card_timer += 1
            if self.flip_card_timer >= 180:
                self.card_manager.flip_cards()
                self.flip_card_timer = 0

            pygame.display.flip()
            self.clock.tick(60)

        pygame.display.quit()
        pygame.quit()
        sys.exit()

######################################################################
