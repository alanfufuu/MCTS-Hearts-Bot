from gamestate import GameState
from player import Player
from card import Suit, Rank, Card
from deck import Deck


playerList = ['Self', 'Bot 1', 'Bot 2', 'Bot 3']
game1 = GameState(playerList)

game1.deal_hands
game1.pass_cards
for player in game1.players:
    print(f'{player.hand}')





