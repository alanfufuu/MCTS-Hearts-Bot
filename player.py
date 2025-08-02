import card

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []
        self.takenHands = []

    def cardsToPass(self, gameState):
        return self.hand[0:3]
    
    def cardToPlay(self, gameState):
        raise NotImplementedError
    
















