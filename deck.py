from card import Suit, Rank, Card
import random


class Deck:
    def __init__(self):
        self.cards = []
        for r in Rank:
            for s in Suit:
                temp = Card(r, s)
                self.cards.append(temp)

    def deal(self, numPlayers = 4, cardsPerPlayer = 13):
        hands = []

        for i in range(numPlayers):
            hand = self.cards[i * cardsPerPlayer : (i + 1) * cardsPerPlayer]
            hands.append(hand)

        self.cards.clear()
        return hands
    
    def shuffle(self) -> None:
        random.shuffle(self.cards)

















