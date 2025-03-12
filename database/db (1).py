import sqlite3 
import random 
import os
import pygame
import pandas as pd

#Get the models
from models.models import *


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
    IMAGE_URL VARCHAR2(255)
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Spells(
    ID INT,
    Number VARCHAR2(255) NOT NULL,
    Name VARCHAR2(255) NOT NULL,
    DECK_COST INT NOT NULL,
    TYPE VARCHAR2(255) NOT NULL,
    EFFECT VARCHAR2(255) NOT NULL
)''')


cur.execute('''CREATE TABLE IF NOT EXISTS Traps(
    ID INT,
    Number VARCHAR2(255) NOT NULL,
    Name VARCHAR2(255) NOT NULL,
    DECK_COST INT NOT NULL,
    TYPE VARCHAR2(255) NOT NULL,
    EFFECT VARCHAR2(255) NOT NULL
)''')



def fetch_random_local_card():
    # Correctly define the categories as a dictionary
    categories = {
        'Monster': 'assets/monsters/',
        'Spell Card': 'assets/spells/',
        'Trap Card': 'assets/traps/'
    }

    # Select a random card type
    card_type = random.choice(list(categories.keys()))
    folder_path = categories[card_type]

    # Choose a random card file from the selected category
    card_file = random.choice(os.listdir(folder_path))
    card_name = os.path.splitext(card_file)[0]
    card_path = os.path.join(folder_path, card_file)

    return card_name, card_path, card_type

def load_image_from_local(path):
    try:
        image = pygame.image.load(path)
        return image
    except pygame.error as e:
        print(f"Error loading image from {path}: {e}")
        return None

def load_cards_from_file(data, card_type): 
    conn = sqlite3.connect("cards.db")
    cursor = conn.cursor()
    
    cards = [] 

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