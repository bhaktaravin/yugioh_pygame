import pygame 
import random 
from database.db import fetch_random_local_card, load_image_from_local



class FloatingCard:
    def __init__(self, back_card_image):
        self.x = random.randint(0, 800)
        self.y = random.randint(-600, 0)
        self.speed = random.uniform(1, 3)
        self.angle = 0
        self.rotation_speed = random.uniform(2, 5)
        self.back_card_image = back_card_image  # Back card image
        self.card_info = {}  # Will hold card information (name, type)
        self.is_flipping = False
        self.flip_direction = 1  # 1 means flipping to back, -1 means flipping to front
        self.flip_progress = 0  # Keeps track of how far the flip has progressed (0 to 100)
        self.flip_duration = 100  # Duration of the flip in terms of frames
        self.front_image = pygame.transform.scale(pygame.image.load(self.fetch_new_card()), (80, 120))

    def update(self):
        self.y += self.speed
        if self.is_flipping:
            self.flip_progress += self.flip_direction
            if self.flip_progress >= self.flip_duration or self.flip_progress <= 0:
                self.flip_direction *= -1  # Reverse the flip direction
                self.flip_progress = max(0, min(self.flip_progress, self.flip_duration))  # Clamp value

        if self.y >= 600:
            self.reset_position() 


    def draw(self, surface):
        # Calculate scaling factor for x-axis to simulate a flip (scale from 1 to -1)
        flip_scale = abs(self.flip_progress / self.flip_duration - 0.5) * 2

        # Determine which image to show (front or back)
        if self.flip_progress < self.flip_duration / 2:
            card_image = self.back_card_image
        else:
            card_image = self.front_image

        # Flip the card horizontally
        scaled_image = pygame.transform.scale(card_image, (int(80 * flip_scale), 120))
        rect = scaled_image.get_rect(center=(self.x, self.y))
        surface.blit(scaled_image, rect.topleft)


    def reset_position(self):
        self.y = random.randint(-120, -20) 
        self.x = random.randint(0, 800)
        self.is_flipping = True 
        self.flip_progress = 0
        self.flip_direction = 1
        self.front_image = pygame.transform.scale(pygame.image.load(self.fetch_new_card()), (80, 120))
    def fetch_new_card(self):
        card_name, card_path, card_type = fetch_random_local_card()
        if card_name and card_path:
            
            new_card_image = load_image_from_local(card_path)
            if new_card_image:
                self.card_image = pygame.transform.scale(new_card_image, (80, 120))
                self.card_info = {'name': card_name, 'type': card_type}
                return card_path

    def flip(self):
        pass