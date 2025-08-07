import enum

class Rank(enum.Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    def __str__(self):
        if(self.value > 10):
            return self.name.capitalize()
        return str(self.value)
    
    def __repr__(self):
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
        return f'{self.rank.name} of {self.suit.value}'
    
    def __repr__(self):
        return f"Card({self.rank!r}, {self.suit!r})"

    def __eq__(self, other):
        if self is other:
            return True
        
        if not isinstance(other, Card):
            return False
        
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))

    def __lt__(self, other):
        if not isinstance(other,Card) or self.suit != other.suit:
            raise TypeError('Cannot compare cards of different suits')
        return self.rank.value < other.rank.value
    

