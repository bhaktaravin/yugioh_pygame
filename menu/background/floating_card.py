import pygame 
import random 
from database.db import fetch_random_local_card, load_image_from_local



class FloatingCard:
    def __init__(self, back_card_image):
        self.x = random.randint(0, 800)
        self.y = random.randint(-600, 0)
        self.speed = random.uniform(0.5, 1.5)
        self.angle = 0
        self.rotation_speed = random.uniform(2, 5)
        self.back_card_image = back_card_image  # Back card image
        self.card_info = {}  # Will hold card information (name, type)
        self.is_flipping = False
        self.flip_direction = 1  # 1 means flipping forward
        self.flip_progress = 0  # Keeps track of how far the flip has progressed (0 to 100)
        self.flip_duration = 90  # Duration of the flip in frames (slower, more dramatic)
        self.front_image = None
        self.card_path = None
        self.show_title = False  # Whether to show title on card
        self.title_timer = 0  # Timer for how long title is shown
        self.title_duration = 120  # Show title for 2 seconds (120 frames at 60fps)
        # Load initial card
        self._load_random_card()
        # Start with a random flip delay
        self.flip_delay = random.randint(0, 180)

    def update(self):
        self.y += self.speed
        
        # Update flip animation
        if self.is_flipping:
            self.flip_progress += self.flip_direction
            if self.flip_progress >= self.flip_duration:
                # Reached front, now flip back
                self.flip_progress = self.flip_duration
                self.flip_direction = -1
            elif self.flip_progress <= 0:
                # Reached back, load new card and flip forward again
                self.flip_progress = 0
                self.flip_direction = 1
                self._load_random_card()  # Load new card when back to backside
        else:
            # Start flipping immediately
            self.is_flipping = True
        
        # Update title display timer
        if self.show_title:
            self.title_timer += 1
            if self.title_timer >= self.title_duration:
                self.show_title = False
                self.title_timer = 0

        # Reset when card goes off screen
        if self.y >= 600:
            self.reset_position() 


    def draw(self, surface):
        if self.front_image is None:
            return
            
        # Calculate flip scale (0 to 1, representing horizontal squish for horizontal flip)
        progress_ratio = self.flip_progress / self.flip_duration
        flip_scale = abs(1 - 2 * progress_ratio)
        
        # Avoid zero-width images
        if flip_scale < 0.01:
            flip_scale = 0.01

        # Determine which image to show (back or front)
        if progress_ratio < 0.5:
            card_image = self.back_card_image
        else:
            card_image = self.front_image

        # Scale the card HORIZONTALLY to simulate horizontal flip
        width = max(1, int(80 * flip_scale))
        scaled_image = pygame.transform.scale(card_image, (width, 120))
        rect = scaled_image.get_rect(center=(self.x, self.y))
        surface.blit(scaled_image, rect.topleft)
        
        # Draw card title if showing
        if self.show_title and self.card_info.get('name'):
            self._draw_title(surface)


    def reset_position(self):
        self.y = random.randint(-120, -20)
        self.x = random.randint(0, 800)
        self.speed = random.uniform(0.5, 1.5)
        self.show_title = False
        self.title_timer = 0
        self.is_flipping = True
        self.flip_progress = 0
        self.flip_direction = 1
        self._load_random_card()
    
    def _draw_title(self, surface):
        """Draw card title below the card"""
        try:
            # Create semi-transparent background for text
            font = pygame.font.Font(None, 20)
            name = self.card_info.get('name', 'Unknown')
            
            # Truncate long names
            if len(name) > 15:
                name = name[:13] + "..."
            
            text = font.render(name, True, (255, 255, 255))
            
            # Create background rect
            padding = 5
            bg_rect = pygame.Rect(
                self.x - text.get_width() // 2 - padding,
                self.y + 65,
                text.get_width() + padding * 2,
                text.get_height() + padding
            )
            
            # Draw semi-transparent background
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(180)
            bg_surface.fill((0, 0, 0))
            surface.blit(bg_surface, bg_rect.topleft)
            
            # Draw text
            text_rect = text.get_rect(center=(self.x, self.y + 70))
            surface.blit(text, text_rect)
        except Exception:
            pass  # Silently fail if font rendering has issues
        
    def _load_random_card(self):
        """Internal method to load a random card image"""
        card_path = self.fetch_new_card()
        if card_path:
            try:
                img = pygame.image.load(card_path)
                self.front_image = pygame.transform.scale(img, (80, 120))
            except Exception as e:
                print(f"Error loading card image: {e}")
                # Use back image as fallback
                self.front_image = self.back_card_image
    def fetch_new_card(self):
        """Fetch a random card and return its path"""
        try:
            card_name, card_path, card_type = fetch_random_local_card()
            if card_name and card_path:
                self.card_info = {'name': card_name, 'type': card_type}
                self.card_path = card_path
                return card_path
        except Exception as e:
            print(f"Error fetching card: {e}")
        return None

    def flip(self):
        """Start the flip animation and load a new card"""
        if not self.is_flipping:
            self.is_flipping = True
            self.flip_progress = 0
            self.flip_direction = 1
            self._load_random_card()