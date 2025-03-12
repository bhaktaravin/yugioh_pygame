from menu.background.floating_card import FloatingCard



class CardManager:
    def __init__(self, back_card_image, num_cards = 10): 
        self.cards = [FloatingCard(back_card_image) for _ in range(num_cards)]


    def update(self): 
        for card in self.cards: 
            card.update() 


    def draw(self, surface): 
        for card in self.cards:
            card.draw(surface) 


    def flip_cards(self): 
        for card in self.cards: 
            card.flip() 


        