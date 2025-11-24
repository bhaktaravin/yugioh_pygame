# Yu-Gi-Oh! Duelist of the Roses - Pygame Remake

A pygame-based remake of the classic Yu-Gi-Oh! Duelist of the Roses game with cloud storage and automated card management.

## Features

- **Main Menu** with animated floating cards (continuous horizontal flip animation)
- **Cloud Storage** - Supabase integration for card images and metadata
- **Excel Sync** - Import 830+ cards from Duelist of the Roses spreadsheet
- **YGOPRODeck API** - Automatic card data and image downloading
- **Progress Tracking** - Visual progress bars for card upload operations
- Card flip animations showing random cards from local or cloud storage
- Menu options: Start Game, Load Game, Deck Builder, Sync Excel to Supabase, Quit
- SQLite database for local card caching with Supabase URLs
- Support for Monsters (683), Spells (118), and Traps (29)

## Recent Features & Optimizations

### Latest Updates (November 2025)
1. **Supabase Cloud Integration**:
   - Cloud storage bucket for card images (monsters, spells, traps)
   - Automated upload from YGOPRODeck API to Supabase
   - SQLite database stores Supabase URLs for quick access
   - Fallback system: local → Supabase → API

2. **Excel Data Sync**:
   - Parse DuelistofTheRoses.xlsx with 830 cards
   - Batch upload with progress tracking UI
   - Threading for background operations (no UI freeze)
   - Menu button "Sync Excel to Supabase" for easy updates

3. **Security Implementation**:
   - Environment variables (.env) for API credentials
   - .gitignore to protect sensitive data
   - python-dotenv integration
   - No hardcoded API keys in source code

4. **Enhanced FloatingCard Animation**:
   - Optimized to 90-frame horizontal flip
   - Continuous flipping with random speeds (0.5-1.5x)
   - Dramatic flip effect for visual appeal
   - CardManager handles 10 simultaneous cards

5. **YGOPRODeck API Client**:
   - Fetch card data by name
   - Download high-quality card images
   - Automatic retry logic for failed downloads
   - Integration with Supabase upload pipeline

### File Structure
```
yugioh/
├── main.py                      # Main entry point
├── test_menu.py                 # Quick menu test script
├── sync_excel_to_supabase.py    # Batch upload 830 cards to cloud
├── test_upload.py               # Test script for 5-card upload
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (API keys) - NOT in git
├── .gitignore                   # Protects sensitive files
├── assets/
│   ├── background.jpg           # Menu background
│   ├── card_back.png            # Card back image
│   ├── excelspreadsheet/
│   │   └── DuelistofTheRoses.xlsx  # 830 card database
│   ├── monsters/                # Local monster card images
│   ├── spells/                  # Local spell card images
│   └── traps/                   # Local trap card images
├── menu/
│   ├── game.py                  # Main game class with sync button
│   ├── menu.py                  # Menu configuration
│   └── background/
│       ├── card_manager.py      # Manages 10 floating cards
│       └── floating_card.py     # Horizontal flip animation (90 frames)
├── database/
│   ├── db.py                    # SQLite + Supabase operations
│   └── supabase_client.py       # Supabase client initialization
├── background/
│   ├── api_client.py            # YGOPRODeck API client
│   ├── downloader.py            # Card image downloader
│   └── logger.py                # Logging utility
├── listofcards/
│   └── getting_all_cards.py     # Excel parser (Monsters, Spells, Traps)
└── entities/
    └── player.py                # Player entity (future use)
```

## Setup & Installation

### 1. Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

Required packages:
- pygame==2.6.1
- pygame_menu==4.5.2
- supabase==2.10.0
- python-dotenv==1.0.0
- requests
- pandas
- openpyxl

### 2. Configure Environment Variables

Create a `.env` file in the project root:
```bash
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key
```

**Important:** Never commit `.env` to version control (already in .gitignore)

### 3. Setup Supabase (Optional)

If using cloud storage:
1. Create a Supabase project at https://supabase.com
2. Create a storage bucket named `yugioh-cards`
3. Create folders: `monsters`, `spells`, `traps`
4. Add your credentials to `.env`

## How to Run

### Quick Test (Main Menu Only)
```bash
python test_menu.py
```

### Full Game with Cloud Sync
```bash
python main.py
```

### Sync Cards to Supabase
```bash
# Option 1: Use menu button (recommended)
python main.py  # Click "Sync Excel to Supabase"

# Option 2: Command line
python sync_excel_to_supabase.py

# Option 3: Test with 5 cards
python test_upload.py
```

## Card Management

### Automatic Card Sync (Recommended)
1. Place `DuelistofTheRoses.xlsx` in `assets/excelspreadsheet/`
2. Run the game: `python main.py`
3. Click "Sync Excel to Supabase" button
4. Wait for progress bar to complete (830 cards)
5. Cards are automatically downloaded from YGOPRODeck API and uploaded to Supabase

### Manual Card Addition
Place card images in the appropriate folders:
- `assets/monsters/` - Monster cards (local cache)
- `assets/spells/` - Spell cards (local cache)
- `assets/traps/` - Trap cards (local cache)

Supported formats: PNG, JPG, JPEG

### Card Loading Priority
1. **Local Cache**: Check `assets/monsters|spells|traps/`
2. **Supabase Cloud**: Fetch from cloud storage if not local
3. **YGOPRODeck API**: Download if not in cloud

## Controls

- **Mouse**: Navigate menu buttons
- **ESC**: Exit menu/game
- Cards automatically flip every 3 seconds in the main menu

## Development Roadmap

### ✅ Completed
- [x] Main menu with animated floating cards
- [x] Card flip animations (90 frames, horizontal)
- [x] SQLite database for card metadata
- [x] Supabase cloud storage integration
- [x] YGOPRODeck API client
- [x] Excel parser for 830 cards
- [x] Batch upload with progress tracking
- [x] Environment variable security
- [x] Local + Cloud card loading system

### 🚧 In Progress
- [ ] Full 830-card sync to Supabase (tested with 5 cards)
- [ ] Game board implementation (7x7 grid)

### 📋 Planned
1. **Game Board**: 7x7 grid matching original Duelist of the Roses
2. **Terrain System**: Different terrain types affect card stats
3. **Card Placement**: Drag-and-drop card positioning
4. **Battle Mechanics**: Attack, defense, fusion summoning
5. **AI Opponent**: Computer player with strategy
6. **Deck Builder UI**: Full interface from menu (currently placeholder)
7. **Save/Load System**: Game state persistence

## Technical Notes

### Performance
- Main menu runs at 60 FPS with 10 animated cards
- Card flip animation: 90 frames for dramatic effect
- Smooth horizontal scaling with speed variation (0.5-1.5x)
- Background card upload doesn't freeze UI (threading)

### Database Architecture
- SQLite stores: card metadata, Supabase URLs, local paths
- Supabase stores: actual card image files (cloud)
- Three-tier loading: Local → Cloud → API
- Tables: Monsters, Spells, Traps with SUPABASE_URL column

### Security
- API credentials in `.env` file (not committed)
- `.gitignore` protects sensitive data
- python-dotenv for environment variable management
- Service role keys never exposed in source code

### Excel Data Source
- File: `DuelistofTheRoses.xlsx`
- Sheets: "Monsters" (683), "Spells" (118), "Traps" (29)
- Total: 830 cards from original game
- Columns: Number, Name, Deck Cost, Attribute, Type, Level, ATK, DEF, Effect

### Cloud Storage
- Provider: Supabase (https://supabase.com)
- Bucket: yugioh-cards (public read access)
- Folders: monsters/, spells/, traps/
- Current cards in cloud: 9 (4 initial + 5 test upload)

## Troubleshooting

### Cards Not Loading
```bash
# Check environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅' if os.getenv('SUPABASE_URL') else '❌')"

# Verify Supabase connection
python -c "from database.supabase_client import get_supabase_client; client = get_supabase_client(); print(client.storage.from_('yugioh-cards').list())"
```

### Upload Issues
- Ensure `.env` has valid credentials
- Check Excel file path: `assets/excelspreadsheet/DuelistofTheRoses.xlsx`
- Verify internet connection for YGOPRODeck API
- Check Supabase storage bucket permissions

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```
