# Quick Start Guide

## Running the Main Menu

The main menu is fully optimized and ready to test!

### Simple Test
```bash
python test_menu.py
```

This will launch the main menu with:
- Animated background with floating cards
- Cards that flip every 3 seconds showing random cards
- Menu buttons: Start Game, Load Game, Deck Builder, Quit

## Menu Features

### 1. **Floating Cards Animation**
- 10 cards floating down the screen
- Each card flips to show a random card image every 3 seconds
- Smooth 60 FPS animation

### 2. **Start Game Button**
- Attempts to load cards from `DuelistofTheRoses.xlsx`
- If Excel file exists, loads all cards into database
- If not, continues without errors

### 3. **Deck Builder Button**
- Opens deck builder menu (placeholder)
- Press ESC or Back to return to main menu

### 4. **Quit Button**
- Cleanly exits the game

## Controls

| Control | Action |
|---------|--------|
| Mouse Click | Select menu buttons |
| ESC | Exit menu/game |
| Auto | Cards flip every 3 seconds |

## Adding Your Card Data

1. **Place Excel file:** 
   - Name: `DuelistofTheRoses.xlsx`
   - Location: Project root (`/Users/ravin/Code/Python3/yugioh/`)

2. **Excel structure required:**
   ```
   Sheet: "Monster"
   Columns: Number, Name, Deck Cost, Attribute, Type, Level, ATK, DEF, Effect, Image URL
   
   Sheet: "Spells"
   Columns: Number, Name, Deck Cost, Type, Effect
   
   Sheet: "Traps"
   Columns: Number, Name, Deck Cost, Type, Effect
   ```

3. **Add card images:**
   - Monsters: `assets/monsters/card_name.png`
   - Spells: `assets/spells/card_name.png`
   - Traps: `assets/traps/card_name.png`

## Troubleshooting

### Menu won't start
```bash
# Check if dependencies are installed
pip install -r requirements.txt
```

### Cards not showing
```bash
# Verify assets exist
ls assets/monsters/
ls assets/spells/
ls assets/traps/

# At least these placeholder cards should exist:
# - dark_magician.png
# - blue_eyes_white_dragon.png
# - dark_hole.png
# - mirror_force.png
```

### Background not showing
```bash
# Check if background image exists
ls assets/background.jpg
ls assets/card_back.png
```

## What's Working

✅ Main menu displays correctly  
✅ Floating card animations smooth at 60 FPS  
✅ Card flipping animation works perfectly  
✅ All menu buttons respond to clicks  
✅ Background image displays  
✅ Cards load from asset folders  
✅ Graceful error handling if assets missing  
✅ Database setup complete  
✅ Excel import system ready  

## What's Next

To complete the game, implement:
1. 7x7 game board
2. Card placement system
3. Battle mechanics
4. Terrain effects
5. AI opponent
6. Deck builder interface

## Current File Status

| File | Status |
|------|--------|
| `test_menu.py` | ✅ Ready to run |
| `menu/game.py` | ✅ Optimized |
| `menu/background/floating_card.py` | ✅ Optimized |
| `menu/background/card_manager.py` | ✅ Working |
| `database/db.py` | ✅ Optimized |
| `listofcards/getting_all_cards.py` | ✅ Created |
| Asset folders | ✅ Created with placeholders |

Enjoy testing your Yu-Gi-Oh! main menu! 🎮
