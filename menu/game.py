import pygame
import pygame_menu
import os
import sys
from menu.background.card_manager import CardManager
from listofcards.getting_all_cards import grab_worksheet_of_monsters, grab_worksheet_of_spells, grab_worksheet_of_traps
from database.db import load_cards_from_file
import upload_to_supabase


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
        self.menu.add.button('Sync Excel to Supabase', self.sync_excel_to_supabase)
        self.menu.add.button('Upload Local Cards', self.upload_local_cards)
        self.menu.add.button('Load Game', self.load_game)
        self.menu.add.button('Deck Builder', self.deckbuilder)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)


################################### SYNC EXCEL TO SUPABASE METHOD #################
    def sync_excel_to_supabase(self):
        """Load cards from Excel and upload to Supabase"""
        self.menu.disable()  # Hide menu during sync
        
        # Show loading text
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        def draw_progress(current, total, card_name):
            self.screen.blit(bg_image, (0, 0))
            
            # Title
            title = font.render("Syncing Cards to Supabase...", True, (255, 255, 255))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
            
            # Progress
            progress_text = small_font.render(f"{current}/{total} cards uploaded", True, (200, 200, 200))
            self.screen.blit(progress_text, (WIDTH//2 - progress_text.get_width()//2, 260))
            
            # Current card
            if card_name:
                card_text = small_font.render(f"Current: {card_name}", True, (150, 150, 255))
                self.screen.blit(card_text, (WIDTH//2 - card_text.get_width()//2, 300))
            
            # Progress bar
            bar_width = 400
            bar_height = 30
            bar_x = WIDTH//2 - bar_width//2
            bar_y = 350
            
            pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
            if total > 0:
                fill_width = int((current / total) * bar_width)
                pygame.draw.rect(self.screen, (50, 200, 50), (bar_x, bar_y, fill_width, bar_height))
            
            pygame.display.flip()
        
        # Import here to avoid blocking menu load
        import threading
        from sync_excel_to_supabase import download_and_upload_cards_from_excel
        
        progress_data = {'current': 0, 'total': 0, 'card_name': '', 'done': False}
        
        def upload_thread():
            try:
                # Monkey-patch print to update progress
                import builtins
                original_print = builtins.print
                
                def progress_print(*args, **kwargs):
                    text = ' '.join(str(arg) for arg in args)
                    if '/' in text and 'Processing' in text:
                        parts = text.split(']')
                        if len(parts) > 1:
                            card_name = parts[1].strip()
                            progress_data['card_name'] = card_name
                    if '✅' in text or 'Uploaded' in text:
                        progress_data['current'] += 1
                    original_print(*args, **kwargs)
                
                builtins.print = progress_print
                
                # Get totals first
                from listofcards.getting_all_cards import grab_worksheet_of_monsters, grab_worksheet_of_spells, grab_worksheet_of_traps
                m = grab_worksheet_of_monsters('DuelistofTheRoses.xlsx', 'assets/excelspreadsheet')
                s = grab_worksheet_of_spells('DuelistofTheRoses.xlsx', 'assets/excelspreadsheet')
                t = grab_worksheet_of_traps('DuelistofTheRoses.xlsx', 'assets/excelspreadsheet')
                progress_data['total'] = len(m) + len(s) + len(t)
                
                download_and_upload_cards_from_excel()
                builtins.print = original_print
            except Exception as e:
                print(f"Error in upload: {e}")
            finally:
                progress_data['done'] = True
        
        # Start upload in background thread
        thread = threading.Thread(target=upload_thread, daemon=True)
        thread.start()
        
        # Update display while uploading
        while not progress_data['done']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
            
            draw_progress(progress_data['current'], progress_data['total'], progress_data['card_name'])
            self.clock.tick(10)  # 10 FPS is enough for progress display
        
        # Show completion
        draw_progress(progress_data['current'], progress_data['total'], 'Complete!')
        pygame.time.wait(2000)
        
        self.menu.enable()  # Show menu again

################################### UPLOAD LOCAL CARDS METHOD #################
    def upload_local_cards(self):
        """Upload local card images to Supabase"""
        print("\n" + "="*50)
        print("Uploading local cards to Supabase...")
        print("="*50)
        
        import upload_to_supabase
        upload_to_supabase.upload_all_cards()
        
        print("\n✅ Upload complete!")
        input("\nPress Enter to return to menu...")

################################### LOAD GAME METHOD #################
    def load_game(self):
        pass


################################### DECK BUILDER METHOD #################
    def deckbuilder(self):
        self.deckbuilder_menu = pygame_menu.Menu('Deck Builder', WIDTH, HEIGHT, theme=self.custom_theme)
        self.deckbuilder_menu.add.button('Back', self.menu)
        self.deckbuilder_menu.mainloop(self.screen)


######################################################################################

################################### START GAME METHOD #################
    def start_game(self):
        print("Starting game...")
        print("Loading cards from Excel file...")
        
        try:
            filename = "DuelistofTheRoses.xlsx"
            search_path = "."
            
            monsters = grab_worksheet_of_monsters(filename, search_path)
            spells = grab_worksheet_of_spells(filename, search_path)
            traps = grab_worksheet_of_traps(filename, search_path)
            
            if not monsters.empty:
                load_cards_from_file(monsters, 'Monster')
            if not spells.empty:
                load_cards_from_file(spells, 'Spells')
            if not traps.empty:
                load_cards_from_file(traps, 'Traps')
                
            print("Cards loaded successfully!")
        except Exception as e:
            print(f"Error loading cards: {e}")
            print("Continuing without loading cards...")
        
        # Close menu to show game would start
        self.menu.disable()

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
