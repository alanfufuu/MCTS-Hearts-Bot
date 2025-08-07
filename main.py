from gamestate import GameState
from player import Player, MCTSPlayer
import random

def playGame():
    playerList = [MCTSPlayer("AI Bot"), Player("Bot 1"), Player("Bot 2"), Player("Bot 3"), ]
    random.shuffle(playerList)
    game1 = GameState(playerList)
    
    while all(p.score < 100 for p in game1.players):
        game1.playRound()
        print("-" * 20)

    winner = min(game1.players, key=lambda p: p.score)
    print(f"\nGame Over! The winner is {winner.name} with a final score of {winner.score}.")
    print("test")

if __name__ == "__main__":
    playGame()

