"""
Helper functions to load card data from Excel file.
Place your DuelistofTheRoses.xlsx in the project root.
"""
import pandas as pd
import os


def find_excel_file(filename, search_path="."):
    """Find the Excel file in the project directory"""
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


def grab_worksheet_of_monsters(filename, search_path="."):
    """
    Load monster cards from the 'Monsters' worksheet.
    
    Expected columns:
    - Number, Name, Deck Cost, Attribute, Type, Level, ATK, DEF, Effect, Image URL
    """
    file_path = find_excel_file(filename, search_path)
    if not file_path:
        print(f"Error: Could not find {filename}")
        return pd.DataFrame()
    
    try:
        df = pd.read_excel(file_path, sheet_name='Monsters')
        print(f"Loaded {len(df)} monster cards")
        return df
    except Exception as e:
        print(f"Error loading monster cards: {e}")
        return pd.DataFrame()


def grab_worksheet_of_spells(filename, search_path="."):
    """
    Load spell cards from the 'Spells' worksheet.
    
    Expected columns:
    - Number, Name, Deck Cost, Type, Effect
    """
    file_path = find_excel_file(filename, search_path)
    if not file_path:
        print(f"Error: Could not find {filename}")
        return pd.DataFrame()
    
    try:
        df = pd.read_excel(file_path, sheet_name='Spells')
        print(f"Loaded {len(df)} spell cards")
        return df
    except Exception as e:
        print(f"Error loading spell cards: {e}")
        return pd.DataFrame()


def grab_worksheet_of_traps(filename, search_path="."):
    """
    Load trap cards from the 'Traps' worksheet.
    
    Expected columns:
    - Number, Name, Deck Cost, Type, Effect
    """
    file_path = find_excel_file(filename, search_path)
    if not file_path:
        print(f"Error: Could not find {filename}")
        return pd.DataFrame()
    
    try:
        df = pd.read_excel(file_path, sheet_name='Traps')
        print(f"Loaded {len(df)} trap cards")
        return df
    except Exception as e:
        print(f"Error loading trap cards: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    # Test the functions
    filename = "DuelistofTheRoses.xlsx"
    
    print("Testing Excel loading functions...")
    monsters = grab_worksheet_of_monsters(filename)
    spells = grab_worksheet_of_spells(filename)
    traps = grab_worksheet_of_traps(filename)
    
    print(f"\nMonsters loaded: {len(monsters)}")
    print(f"Spells loaded: {len(spells)}")
    print(f"Traps loaded: {len(traps)}")
    
    if not monsters.empty:
        print("\nFirst monster:")
        print(monsters.head(1))
