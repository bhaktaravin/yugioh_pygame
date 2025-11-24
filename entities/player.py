class Player:
    def __init__(self, name):
        self.name = name, 
        self.health = 8000
        self.hand = []
        self.deck = []
        self.field = []

    def draw_card(self):
        if self.deck:
            card = self.deck.pop()
            self.hand.append(card)
            return card
        return None

    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            self.field.append(card)
            return True
        return False

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount

    def get_hand(self):
        return self.hand

    def get_health(self):
        return self.health

    def set_deck(self, deck):
        self.deck = deck

    def clear_field(self):
        self.field.clear()