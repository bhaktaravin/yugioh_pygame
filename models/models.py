class Card:
    def __init__(self, card_type):
        self.card_type = card_type  # Base type (e.g., 'Monster', 'Spell', 'Trap')
        self.number = number
        self.name = name
        self.deck_cost = deck_cost

    def __repr__(self):
        return f"{self.card_type}"


class Monster(Card):
    def __init__(self, number, name, deck_cost, attribute, card_type, level, atk, def_, effect, image_url):
        super().__init__('Monster')
        self.attribute = attribute
        self.type = card_type  # Use 'type' as a property name, not as an attribute
        self.level = level
        self.atk = atk
        self.def_ = def_
        self.effect = effect
        self.image_url = image_url

    def __repr__(self):
        return (f"Monster(Number: {self.number}, Name: {self.name}, Deck Cost: {self.deck_cost}, "
                f"Attribute: {self.attribute}, Type: {self.type}, Level: {self.level}, "
                f"ATK: {self.atk}, DEF: {self.def_}, Effect: {self.effect}, Image URL: {self.image_url})")


class Spell(Card):
    def __init__(self, number, name, deck_cost, spell_type, effect):
        super().__init__('Spell', number, name, deck_cost)
        self.spell_type = spell_type
        self.effect = effect

    def __repr__(self):
        return (f"Spell(Number: {self.number}, Name: {self.name}, Deck Cost: {self.deck_cost}, "
                f"Type: {self.spell_type}, Effect: {self.effect})")


class Trap(Card):
    def __init__(self, number, name, deck_cost, trap_type, effect):
        super().__init__('Trap', number, name, deck_cost)
        self.trap_type = trap_type
        self.effect = effect

    def __repr__(self):
        return (f"Trap(Number: {self.number}, Name: {self.name}, Deck Cost: {self.deck_cost}, "
                f"Type: {self.trap_type}, Effect: {self.effect})")
