from card import Rank, Suit, Card
from deck import Deck
from player import Player


class GameState:
    def __init__(self, playerList):
        self.players = [Player(name) for name in playerList]
        self.deck = Deck()
        self.hearts_broken = False
        self.round_number = 1
        self.previous_tricks = []
        self.current_trick = []
        self.pass_direction = None
        self.currPlayerIndex = 0

        
    def deal_hands(self) -> None:
        self.deck.shuffle()
        
        dealt_hands = self.deck.deal()

        for i, hand in enumerate(dealt_hands):
            self.players[i].hand = hand

            self.players[i].hand.sort(key=lambda card: (card.suit.value, card.rank.value))

    
    def pass_cards(self):
        #determine pass direction
        #collect cards to pass (player method)
        #pass the cards, update the hands
        directions = {
            0 : 0,
            1 : 1,
            2 : -1,
            3: 2
        }
        self.pass_direction = directions[self.round_number % 4]
        
        cardsToPass = [[] for _ in range(len(self.players))]
        for i, player in enumerate(self.players):
            temp = player.cardsToPass(self)

            for ii in temp:
                player.hand.remove(ii)

            cardsToPass[i] = temp

        for i in range(len(self.players)):
            receivingIndex = (i + self.pass_direction) % len(self.players)

            self.players[receivingIndex].hand.extend(cardsToPass[i])

            self.players[receivingIndex].hand.sort(key=lambda card: (card.suit.value, card.rank.value))

        















