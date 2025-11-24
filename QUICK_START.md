# Quick Start Guide

## Prerequisites

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment (if using cloud storage)**
Create `.env` file:
```bash
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_service_role_key
```

## Running the Main Menu

The main menu is fully optimized with cloud storage integration!

### Quick Test (No Cloud Required)
```bash
python test_menu.py
```

This will launch the main menu with:
- Animated background with 10 floating cards
- Cards continuously flip showing random images from local or cloud
- Menu buttons: Start Game, Load Game, Deck Builder, **Sync Excel to Supabase**, Quit

## Menu Features

### 1. **Floating Cards Animation**
- 10 cards floating down the screen
- Continuous horizontal flip animation (90 frames)
- Variable speeds (0.5-1.5x) for dynamic effect
- Loads cards from: Local assets → Supabase cloud → YGOPRODeck API
- Smooth 60 FPS rendering

### 2. **Start Game Button**
- Launches game board (placeholder - under development)
- Future: 7x7 grid with card placement

### 3. **Deck Builder Button**
- Opens deck builder menu (placeholder)
- Press ESC or Back to return to main menu
- Future: Full card collection browser and deck editor

### 4. **Sync Excel to Supabase Button** ⭐ NEW
- Uploads 830 cards from Excel to cloud storage
- Downloads card images from YGOPRODeck API
- Shows progress bar during upload
- Runs in background thread (no UI freeze)
- Updates SQLite database with Supabase URLs

### 5. **Quit Button**
- Cleanly exits the game

## Controls

| Control | Action |
|---------|--------|
| Mouse Click | Select menu buttons |
| ESC | Exit menu/game |
| Auto | Cards flip every 3 seconds |

## Syncing Card Data

### Automatic Sync (Recommended) ⭐

1. **Ensure Excel file exists:**
   - Path: `assets/excelspreadsheet/DuelistofTheRoses.xlsx`
   - Contains: 683 monsters, 118 spells, 29 traps

2. **Configure Supabase (one-time setup):**
   - Create project at https://supabase.com
   - Create storage bucket: `yugioh-cards`
   - Add folders: `monsters`, `spells`, `traps`
   - Copy URL and service role key to `.env`

3. **Run sync:**
   ```bash
   # Option A: Use menu (recommended)
   python main.py
   # Click "Sync Excel to Supabase" button
   
   # Option B: Command line
   python sync_excel_to_supabase.py
   
   # Option C: Test with 5 cards first
   python test_upload.py
   ```

4. **What happens:**
   - ✅ Reads card names from Excel
   - ✅ Downloads card images from YGOPRODeck API
   - ✅ Uploads images to Supabase cloud storage
   - ✅ Updates SQLite with Supabase URLs
   - ✅ Shows progress bar (e.g., "Uploading: 450/830")

### Manual Method (Local Only)

1. **Excel structure:**
   ```
   Sheet: "Monsters" (note: plural)
   Columns: Number, Name , Deck Cost, Attribute, Type, Level, ATK, DEF, Effect
            (note: "Name " has trailing space in Excel)
   
   Sheet: "Spells"
   Columns: Number, Name, Deck Cost, Type, Effect
   
   Sheet: "Traps"
   Columns: Number, Name, Deck Cost, Type, Effect
   ```

2. **Add card images manually:**
   - Monsters: `assets/monsters/card_name.png`
   - Spells: `assets/spells/card_name.png`
   - Traps: `assets/traps/card_name.png`

## Troubleshooting

### Menu won't start
```bash
# Check if dependencies are installed
pip install -r requirements.txt

# Verify python-dotenv is installed
pip show python-dotenv
```

### Environment Variables Not Loading
```bash
# Test .env file
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('SUPABASE_URL:', os.getenv('SUPABASE_URL'))"

# Expected output:
# SUPABASE_URL: https://your-project.supabase.co

# If empty, check:
# 1. .env file exists in project root
# 2. .env has correct format (no quotes needed):
#    SUPABASE_URL=https://...
#    SUPABASE_KEY=eyJ...
```

### Cards not showing
```bash
# Check local assets
ls assets/monsters/
ls assets/spells/
ls assets/traps/

# Check Supabase connection
python -c "from database.supabase_client import get_supabase_client; print(get_supabase_client().storage.from_('yugioh-cards').list())"

# Expected output: List of files in cloud storage
```

### Upload fails
```bash
# Verify Excel file exists
ls assets/excelspreadsheet/DuelistofTheRoses.xlsx

# Check YGOPRODeck API
curl -s "https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark%20Magician" | python -m json.tool

# Expected: JSON response with card data
```

### Background not showing
```bash
# Check if background images exist
ls assets/background.jpg
ls assets/card_back.png
```

## What's Working

✅ Main menu displays correctly  
✅ Floating card animations smooth at 60 FPS (90-frame horizontal flip)  
✅ Card flipping animation with variable speeds (0.5-1.5x)  
✅ All menu buttons respond to clicks  
✅ Background image displays  
✅ Cards load from local assets, Supabase cloud, or API  
✅ Graceful error handling if assets missing  
✅ Database setup complete (SQLite + Supabase)  
✅ Excel import system (830 cards)  
✅ YGOPRODeck API integration  
✅ Supabase cloud storage  
✅ Batch upload with progress tracking  
✅ Environment variable security (.env)  
✅ Threading for background uploads (no UI freeze)  
✅ Tested upload (5 cards successful)  

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
