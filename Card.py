import random
import config

class Card:
    def __init__(self):
        self.value = random.randint(config.VAL_START, config.VAL_END)
        self.suit = random.choice(config.SUITS)

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit

    def displayCard(self):
        return f"{"K" if self.value == 13 else "Q" if self.value == 12 else "J" if self.value == 11 else self.value} OF {self.suit}"