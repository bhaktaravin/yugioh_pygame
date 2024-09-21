import requests 
from io import BytesIO
import random 


def fetch_random_card(): 
    url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
    param = {
        'type': random.choice(['Monster', 'Spell Card', 'Trap Card', 'Ritual'])
    }


    response = requests.get(url, params=params) 
    if response.status.code ==200: 
        data = response.json() 

        
        