import enum

class Rank(enum.Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        if(self.value > 10):
            return self.name.capitalize()
        return str(self.value)
    
    def _repr__(self):
        return f'Rank.{self.name}'



class Suit(enum.Enum): 
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    SPADES = "Spades"

    def __str__(self):
        return f'{self.value}'
    
class Card:
    def __init__(self, rank : Rank, suit : Suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank.value} of {self.suit.value}'
    
    def __repr__(self):
        return f"Card({self.rank!r}, {self.suit!r})"

    def __eq__(self, other):
        if self is other:
            return True
        
        if not isinstance(self, other):
            return False
        
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash(self.rank, self.suit)

    def __lt__(self, other):
        if not isinstance(other,Card) or self.Suit != other.Suit:
            raise TypeError('Cannot compare cards of different suits')
        return self.rank.value < other.rank.value
    




    













