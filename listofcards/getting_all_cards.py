
# Getting All the cards from a local Excel File 

import pandas as pd
import sys 
import os 




def find_file_of_cards(filename, search_path): 
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None
    #monsters = pd.read_excel('DuelistofTheRoses.xlsx', sheet_name="Monsters")
    #print(monsters.head())
    

    #insert_file_of_cards(monsters)
    

def parse_file_of_cards(filename, search_path):
    file_path = find_file_of_cards(filename, search_path)
    if file_path is None:
        print("File not found")
        sys.exit(1)
    else:
        return file_path


def grab_worksheet_of_monsters(filename, search_path):
    file_path = parse_file_of_cards(filename, search_path)
    monsters = pd.read_excel(file_path, sheet_name="Monsters")
    
    #for index, row in monsters.iterrows():
        #print(row)

    return monsters

    

def grab_worksheet_of_spells(filename, search_path):
    file_path = parse_file_of_cards(filename, search_path)
    spells = pd.read_excel(file_path, sheet_name="Spells")
    
    return spells

def grab_worksheet_of_traps(filename, search_path):

    file_path = parse_file_of_cards(filename, search_path)
    traps = pd.read_excel(file_path, sheet_name="Traps")
    
    return traps

def grab_worksheet_of_rituals(filename, search_path):
    file_path = parse_file_of_cards(filename, search_path) 

    rituals = pd.read_excel(file_path, sheet_name="Rituals")

    return rituals


