# Yu-Gi-Oh! Duelist of the Roses - Pygame Remake

A pygame-based remake of the classic Yu-Gi-Oh! Duelist of the Roses game.

## Features

- **Main Menu** with animated floating cards
- Card flip animations showing random cards from your collection
- Menu options: Start Game, Load Game, Deck Builder, Quit
- SQLite database for card management
- Support for Monsters, Spells, and Traps

## Recent Optimizations

### Code Improvements
1. **Fixed imports** - Removed non-existent module dependencies
2. **Improved FloatingCard class**:
   - Better error handling for missing card images
   - Smoother flip animation (60 frames)
   - Graceful fallback to card back if images are missing
   - Optimized image loading
3. **Database improvements**:
   - Added checks for empty card folders
   - Better error handling in `fetch_random_local_card()`
   - Removed unused imports
4. **Game class**:
   - Simplified start_game method
   - Added proper sys import for clean exit
   - Fixed menu flow

### File Structure
```
yugioh/
├── main.py              # Main entry point
├── test_menu.py         # Quick menu test script
├── requirements.txt     # Python dependencies
├── assets/
│   ├── background.jpg   # Menu background
│   ├── card_back.png    # Card back image
│   ├── monsters/        # Monster card images
│   ├── spells/          # Spell card images
│   └── traps/           # Trap card images
├── menu/
│   ├── game.py          # Main game class
│   └── background/
│       ├── card_manager.py    # Manages multiple floating cards
│       └── floating_card.py   # Individual card animation
├── database/
│   └── db.py            # SQLite database operations
└── background/
    ├── downloader.py    # Card image downloader
    └── logger.py        # Logging utility
```

## How to Run

### Quick Test (Main Menu Only)
```bash
python test_menu.py
```

### Full Game
```bash
python main.py
```

## Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- pygame
- pygame_menu
- beautifulsoup4 (bs4)
- requests
- pandas

## Adding Card Images

Place card images in the appropriate folders:
- `assets/monsters/` - Monster cards
- `assets/spells/` - Spell cards
- `assets/traps/` - Trap cards

Supported formats: PNG, JPG, JPEG

## Controls

- **Mouse**: Navigate menu buttons
- **ESC**: Exit menu/game
- Cards automatically flip every 3 seconds in the main menu

## Next Steps

To implement the full game from the Excel data:
1. Create `listofcards/getting_all_cards.py` with functions:
   - `grab_worksheet_of_monsters(filename, search_path)`
   - `grab_worksheet_of_spells(filename, search_path)`
   - `grab_worksheet_of_traps(filename, search_path)`
2. Place your `DuelistofTheRoses.xlsx` file in the project root
3. Implement game board (7x7 grid) in `menu/game.py`
4. Add terrain system (matching Duelist of the Roses)
5. Implement card placement and battle mechanics

## Notes

- The main menu is fully functional and optimized
- Placeholder cards are used for testing
- Database schema is set up and ready for card data
- Card flip animations work smoothly at 60 FPS
