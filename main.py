from gamestate import GameState
from player import Player, MCTSPlayer, humanPlayer
import random

def playBotGame():
    playerList = [MCTSPlayer("AI Bot"), Player("Self"), Player("Bot 2"), Player("Bot 3"), ]
    random.shuffle(playerList)
    game1 = GameState(playerList)
    
    while all(p.score < 100 for p in game1.players):
        game1.playRound()

        print("-" * 20)
        

    winner = min(game1.players, key=lambda p: p.score)
    print(f"\nGame Over! The winner is {winner.name} with a final score of {winner.score}.")

def playHumanGame():
    playerList = [MCTSPlayer("AI Bot 1"), humanPlayer("Self"), MCTSPlayer("AI Bot 2"), MCTSPlayer("AI Bot 3"), ]
    random.shuffle(playerList)
    game1 = GameState(playerList)
    
    while all(p.score < 100 for p in game1.players):
        game1.playRound()
        print("-" * 20)

    winner = min(game1.players, key=lambda p: p.score)
    print(f"\nGame Over! The winner is {winner.name} with a final score of {winner.score}.")


if __name__ == "__main__":
    while True:
        user_input = input("Would you like to simulate a bot game or play a game yourself? (Reply 'bot' or 'self')\n")

        if user_input == 'bot':
            print(f"Starting simulation of an AI trained bot verses three bots that play random legal cards")
            playBotGame()
            break
        elif user_input == 'self':
            print(f"Starting game against three AI bots")
            playHumanGame()
            break
        else:
            print(f"Invalid input: Please reply with either 'bot' or 'self'")



