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
        return f'{self.rank.name} of {self.suit.name}'
    
    def __repr__(self):
        return f'Rank.{self.name}'



class Suit(enum.Enum): 
    Clubs = 0
    Diamonds = 1
    Hearts = 2
    Spades = 3

    def __str__(self):
        return f'{self.name}'
    
class Card:
    def __init__(self, rank : Rank, suit : Suit):
        self.rank = rank
        self.suit = suit

    @classmethod
    def from_string(cls, string_rep : str): #from 2H, 4S, etc

        if len(string_rep) == 3:
            srank = string_rep[:2]
            ssuit = string_rep[2]
        else:
            srank = string_rep[0]
            ssuit = string_rep[1]

        if srank.isdigit():
            rank = Rank(int(srank))
        elif srank.upper() == 'J':
            rank = Rank.Jack
        elif srank.upper() == 'Q':
            rank = Rank.Queen
        elif srank.upper() == 'K':
            rank = Rank.King
        elif srank.upper() == 'A':
            rank = Rank.Ace
        else:
            raise ValueError(f"Invalid rank string: {srank}")

        suits = {
            'C': Suit.Clubs,
            'D': Suit.Diamonds,
            'H': Suit.Hearts,
            'S': Suit.Spades,
        }
        suit = suits.get(ssuit.upper())
        if not suit:
            raise ValueError(f"Invalid suit string: {ssuit}")
        return cls(rank, suit)

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
    

