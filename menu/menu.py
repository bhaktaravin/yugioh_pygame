import pygame
import pygame_menu
import random
import os
from database.db import fetch_random_local_card, load_image_from_local


# Global constants
WIDTH, HEIGHT = 800, 600

# Function to get the full file path
def get_full_path(file_name):
    return os.path.abspath(file_name)

# Initialize Pygame
pygame.init()

# Load images and handle missing files
bg_image_path = get_full_path('assets/background.jpg')
card_image_path = get_full_path('assets/card_back.png')

# Print file paths for debugging
print(f"Background image path: {bg_image_path}")
print(f"Card image path: {card_image_path}")

try:
    bg_image = pygame.image.load(bg_image_path)
    back_card_image = pygame.image.load(card_image_path)
    
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# Scale the card image to the desired size
back_card_image = pygame.transform.scale(back_card_image, (80, 120))

# FloatingCard class
class FloatingCard:

    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(1, 3)
        self.angle = 0
        self.rotation_speed = random.uniform(2, 5)
        self.back_card_image = back_card_image  # Back card image
        self.card_info = {}  # Will hold card information (name, type)
        self.is_flipping = False
        self.flip_direction = 1  # 1 means flipping to back, -1 means flipping to front
        self.flip_progress = 0  # Keeps track of how far the flip has progressed (0 to 100)
        self.flip_duration = 100  # Duration of the flip in terms of frames
        self.is_front = True  # Start by showing the front of the card' 
        self.card_info = {} 
        self.front_image = pygame.transform.scale(pygame.image.load(front_image_path, (80,120)))


    def update(self):
        self.y += self.speed

        # Update the flip progress if the card is flipping
        if self.is_flipping:
            self.flip_progress += self.flip_direction
            if self.flip_progress >= self.flip_duration:
                self.flip_progress = self.flip_duration
                self.is_flipping = False
                self.is_front = not self.is_front  # Toggle between front and back
            elif self.flip_progress <= 0:
                self.flip_progress = 0
                self.is_flipping = False
                self.is_front = not self.is_front  # Toggle between front and back

        if self.y > HEIGHT:
            self.__init__()

    def draw(self, surface):
        # Calculate scaling factor for x-axis to simulate a flip (scale from 1 to -1)
        flip_scale = 1 - 2 * abs(self.flip_progress / self.flip_duration - 0.5)

        # If the card is near the middle of the flip, show the back (info) side
        if flip_scale < 0 and not self.is_front:
            self.show_card_info(surface)
        else:
            # Draw the front or back based on the current flip progress
            rotated_image = pygame.transform.rotate(self.card_image, self.angle)
            scaled_image = pygame.transform.scale(rotated_image, (int(80 * abs(flip_scale)), 120))
            rect = scaled_image.get_rect(center=(self.x, self.y))
            surface.blit(scaled_image, rect.topleft)

    # Function to show card info when the card is "flipped"
    def show_card_info(self, surface):
        font = pygame.font.SysFont('Arial', 24, bold=True)
        text_color = (255, 255, 255)  # White text

        card_info_rect = pygame.Rect(self.x - 40, self.y - 60, 80, 120)  # Card back rectangle
        pygame.draw.rect(surface, (0, 0, 0), card_info_rect)  # Black background for info

        # Draw the card name and type centered in the rectangle
        name_text = font.render(self.card_info.get('name', 'Unknown'), True, text_color)
        type_text = font.render(self.card_info.get('type', 'Card'), True, text_color)

        surface.blit(name_text, (self.x - name_text.get_width() // 2, self.y - 40))
        surface.blit(type_text, (self.x - type_text.get_width() // 2, self.y + 10))

    def fetch_new_card(self):
        card_name, card_path, card_type = fetch_random_local_card()
        if card_name and card_path:
            print(f"Fetching new card: {card_name} ({card_type})")

            # Save the card details to the appropriate database table
            save_card_to_db(card_name, card_path, card_type)

            # Load the new card image from the local file
            new_card_image = load_image_from_local(card_path)
            if new_card_image:
                self.card_image = pygame.transform.scale(new_card_image, (80, 120))
                self.card_info = {'name': card_name, 'type': card_type}

    # Function to initiate a flip
    def flip(self):
        if not self.is_flipping:
            self.is_flipping = True
            self.flip_direction *= -1  # Reverse the flip direction each time




def start_game():
    print("Game started!")
    # Implement the game logic here


def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Yu-Gi-Oh! Duel Menu')

    cards = [FloatingCard() for _ in range(10)]
    clock = pygame.time.Clock()

    # Customizing the menu theme to match the background
    custom_theme = pygame_menu.themes.THEME_DARK.copy()
    custom_theme.background_color = (0, 0, 0, 0)
    # Create the menu using pygame_menu
    menu = pygame_menu.Menu('Yu-Gi-Oh! Duel Menu', WIDTH, HEIGHT, theme=custom_theme)
    menu.add.button('Start Game', start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    running = True
    fetch_new_card_timer = 0
    flip_card_timer = 0



    while running:
        # First draw the background (via the menu's theme) and floating cards
        screen.blit(bg_image, (0, 0))  # Draw the background

        for card in cards:
            card.update()
            card.draw(screen)

        # Handle menu events and draw the menu
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Update and draw the menu on top of the background and cards
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

             flip_card_timer += 1
        if flip_card_timer >= 180:  # Flip every 3 seconds (60 FPS * 3 = 180)
            for card in cards:
                card.flip()
            flip_card_timer = 0

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
