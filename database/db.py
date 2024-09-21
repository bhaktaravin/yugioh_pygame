import sqlite3 


conn = sqlite3.connect("cards.db") 


cur = conn.cursor()


#cur.execute('''CREATE TABLE IF NOT EXISTS Monster(
#    ID INT,
#    Number VARCHAR2(255) NOT NULL, 
#    Name VARCHAR2(255) NOT NULL,
#    DECK_COST INT NOT NULL,
#    ATTRIBUTE VARCHAR2(255) NOT NULL,  
#    TYPE VARCHAR2(255) NOT NULL,
#    LEVEL VARCHAR2(255) NOT NULL, 
#    ATK INT NOT NULL, 
#    DEF INT NOT NULL,
#    EFFECT VARCHAR2(255),
#    IMAGE_URL VARCHAR2(255)
#)''')

#cur.execute('''CREATE TABLE IF NOT EXISTS Spells(
#    ID INT,
#    Number VARCHAR2(255) NOT NULL, 
#    Name VARCHAR2(255) NOT NULL,
#    DECK_COST INT NOT NULL, 
#    TYPE VARCHAR2(255) NOT NULL,
#    EFFECT VARCHAR2(255) NOT NULL,    
#)''')


#cur.execute('''CREATE TABLE IF NOT EXISTS Traps(
#    ID INT,
#    Number VARCHAR2(255) NOT NULL, 
#    Name VARCHAR2(255) NOT NULL,
#    DECK_COST INT NOT NULL, 
#    TYPE VARCHAR2(255) NOT NULL,
#    EFFECT VARCHAR2(255) NOT NULL,    
#)''')



def fetch_random_local_card(): 
    categories: {
        'Monster':'assets/monsters/',
        'Spell Card': 'assets/spells/',
        'Trap Card': 'assets/traps/'
    }

    card_type = random.choice(list(categories.keys()))
    folder_path = categories[card_type]


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

