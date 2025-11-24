import sqlite3 
import random 
import os
import pygame
import pandas as pd
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://toonzkjgytoknfruuqvo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRvb256a2pneXRva25mcnV1cXZvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDAwNTg1MCwiZXhwIjoyMDc5NTgxODUwfQ.EI-xRmpx7PyIohLVv5XT06Yh4OwiWVYHEHEEVcsVE4g"
STORAGE_BUCKET = "yugioh-cards"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


conn = sqlite3.connect("cards.db") 


cur = conn.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS Monster(
    ID INT,
    Number VARCHAR2(255),
    Name VARCHAR2(255) ,
    DECK_COST INT ,
    ATTRIBUTE VARCHAR2(255) ,
    TYPE VARCHAR2(255) ,
    LEVEL VARCHAR2(255) ,
    ATK INT ,
    DEF INT ,
    EFFECT VARCHAR2(255),
    IMAGE_URL VARCHAR2(255),
    SUPABASE_URL VARCHAR2(255)
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Spells(
    ID INT,
    Number VARCHAR2(255) NOT NULL,
    Name VARCHAR2(255) NOT NULL,
    DECK_COST INT NOT NULL,
    TYPE VARCHAR2(255) NOT NULL,
    EFFECT VARCHAR2(255) NOT NULL,
    SUPABASE_URL VARCHAR2(255)
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Traps(
    ID INT,
    Number VARCHAR2(255) NOT NULL,
    Name VARCHAR2(255) NOT NULL,
    DECK_COST INT NOT NULL,
    TYPE VARCHAR2(255) NOT NULL,
    EFFECT VARCHAR2(255) NOT NULL,
    SUPABASE_URL VARCHAR2(255)
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS CardImages(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id INT,
    image_name VARCHAR2(255),
    image_path VARCHAR2(255),
    image_url VARCHAR2(255),
    download_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (card_id) REFERENCES Monster(ID)
)''')


def list_supabase_cards(folder='monsters'):
    """List all cards in Supabase storage bucket"""
    try:
        result = supabase.storage.from_(STORAGE_BUCKET).list(folder)
        return result
    except Exception as e:
        print(f"Error listing cards from Supabase: {e}")
        return []


def get_supabase_image_url(storage_path):
    """Get public URL for a card image from Supabase"""
    try:
        public_url = supabase.storage.from_(STORAGE_BUCKET).get_public_url(storage_path)
        return public_url
    except Exception as e:
        print(f"Error getting Supabase URL: {e}")
        return None


def fetch_random_local_card():
    """Fetch random card from local assets OR Supabase"""
    # Correctly define the categories as a dictionary
    categories = {
        'Monster': 'monsters',
        'Spell Card': 'spells',
        'Trap Card': 'traps'
    }

    # Select a random card type
    card_type = random.choice(list(categories.keys()))
    folder = categories[card_type]
    
    # First try local files
    local_folder = f'assets/{folder}/'
    
    # Check if folder exists and has files
    if os.path.exists(local_folder):
        files = [f for f in os.listdir(local_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if files:
            # Use local file
            card_file = random.choice(files)
            card_name = os.path.splitext(card_file)[0]
            card_path = os.path.join(local_folder, card_file)
            return card_name, card_path, card_type
    
    # If no local files, try Supabase
    supabase_files = list_supabase_cards(folder)
    if supabase_files:
        random_file = random.choice(supabase_files)
        card_name = os.path.splitext(random_file['name'])[0]
        storage_path = f"{folder}/{random_file['name']}"
        supabase_url = get_supabase_image_url(storage_path)
        
        # Download image temporarily for pygame
        if supabase_url:
            return card_name, supabase_url, card_type
    
    # Fallback to card back
    print(f"Warning: No cards found in {folder}")
    return "Unknown Card", "assets/card_back.png", card_type

def load_image_from_local(path):
    """Load image from local file or URL (Supabase)"""
    try:
        # Check if it's a URL
        if path.startswith('http'):
            import io
            import requests
            response = requests.get(path)
            response.raise_for_status()
            image_data = io.BytesIO(response.content)
            image = pygame.image.load(image_data)
            return image
        else:
            # Local file
            image = pygame.image.load(path)
            return image
    except Exception as e:
        print(f"Error loading image from {path}: {e}")
        return None

def load_cards_from_file(data, card_type): 
    conn = sqlite3.connect("cards.db")
    cursor = conn.cursor()

    for i in range(len(data)):
        card = data.iloc[i]

        print(card)

        if card_type == 'Monster':
            cursor.execute("INSERT INTO Monster VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (i,card[0], card[1], card[2], card[3], card[4], card[5], card[6], card[7], card[8], card[9]))
        elif card_type == 'Spells':
            cursor.execute("INSERT INTO Spells VALUES (?, ?, ?, ?, ?, ?)",
            (i, card[0], card[1], card[2], card[3], card[4]))
        elif card_type == 'Traps':
            cursor.execute("INSERT INTO Traps VALUES (?, ?, ?, ?, ?, ?)",
            (i, card[0], card[1], card[2], card[3], card[4]))

    conn.commit()
    conn.close()


    #print(type(data))

    #for index, row in data.iterrows(): 

        
        #print(f"Row Data: {row}, Type of row: {type(row)}")

        #if card_type == 'Monster':
            #print("Index: ", index, "Row: ", row[index])
            
           
      
        #### DEBUGGING #####


def print_array(arr): 
    for data in arr: 
        print(data)
    #print(f"Row data: {row}, Type of row: {type(row)}")
    

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def upload_card_to_supabase(local_path, card_name, card_type):
    """
    Upload a card image to Supabase storage
    
    Args:
        local_path: Local file path to the image
        card_name: Name of the card
        card_type: 'Monster', 'Spell Card', or 'Trap Card'
    
    Returns:
        Public URL of the uploaded image
    """
    folder_map = {
        'Monster': 'monsters',
        'Spell Card': 'spells',
        'Trap Card': 'traps'
    }
    folder = folder_map.get(card_type, 'monsters')
    
    # Clean filename
    clean_name = card_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    storage_path = f"{folder}/{clean_name}.jpg"
    
    try:
        with open(local_path, "rb") as f:
            supabase.storage.from_(STORAGE_BUCKET).upload(
                file=f,
                path=storage_path,
                file_options={"content-type": "image/jpeg", "upsert": "true"}
            )
        
        # Get public URL
        public_url = get_supabase_image_url(storage_path)
        print(f"✅ Uploaded {card_name} to Supabase: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Error uploading {card_name} to Supabase: {e}")
        return None


def save_image_details(card_id, image_name, image_path, image_url):
    try:
        cur.execute('''INSERT INTO CardImages (card_id, image_name, image_path, image_url)
                      VALUES (?, ?, ?, ?)''', (card_id, image_name, image_path, image_url))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error saving image details: {e}")
        return False