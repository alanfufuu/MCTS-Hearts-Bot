from card import Rank, Suit
from deck import Deck
from player import Player


class GameState:
    def __init__(self, playerList):
        self.players = [Player(name) for name in playerList]
        self.deck = Deck()
        self.hearts_broken = False
        self.hand_number = 1
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
        self.pass_direction = directions[(self.hand_number - 1) % 4]
        
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

    def findLeader(self):
        for i, player in enumerate(self.players):
            for card in player.hand:
                if card.suit == Suit.CLUBS and card.rank == Rank.Two:
                    self.currPlayerIndex = i
                    print(f"The leader for this hand is {player.name} with the 2 of Clubs")
                    return
                
    def legal_moves(self):
        #hearts broken, suit check. self.player[currPlayerIndex].legal_moves returns a list of the legal cards in their hand
        firstTrick = len(self.previous_tricks) == 0
        playerHand = self.players[self.currPlayerIndex].hand

        if not self.current_trick: #if the current trick is empty, aka the leader
            if firstTrick: #lead
                return [card for card in playerHand if card.suit == Suit.CLUBS and card.rank == Rank.Two]
            else:
                if not self.hearts_broken:
                    nonHearts = [card for card in playerHand if card.suit != Suit.HEARTS]
                    if nonHearts:
                        return nonHearts
                    else:
                        self.hearts_broken = True
                        return playerHand
                else:
                    return playerHand
        else: #if not the leader
            initialSuit = self.current_trick[0][0].suit

            initialSuitCards = [card for card in playerHand if card.suit == initialSuit]

            if initialSuitCards:
                if firstTrick:
                    nonPointInitialSuit = [card for card in initialSuitCards if not (card.suit == Suit.HEARTS or (card.suit == Suit.SPADES and card.rank == Rank.Queen))]
                    if nonPointInitialSuit:
                        return nonPointInitialSuit
                    else: 
                        return initialSuitCards
                else:
                    return initialSuitCards
            else:
                if firstTrick:
                    nonPoints = [card for card in playerHand if not (card.suit == Suit.HEARTS or (card.suit == Suit.SPADES and card.rank == Rank.Queen))]
                    if nonPoints:
                        return nonPoints
                    else:
                        return playerHand
                else:
                    return playerHand
                
    def playTrick(self):
        #call each player's choose card to play function, add to curr trick
        if self.current_trick:
            self.current_trick.clear()
        
        numPlayers = len(self.players)
        leader_index = self.currPlayerIndex

        for i in range(numPlayers):
            curr_player_index = (leader_index + i) % numPlayers
            self.currPlayerIndex = curr_player_index
            curr_player = self.players[self.currPlayerIndex]

            legal_moves = self.legal_moves()

            chosenCard = curr_player.cardToPlay(self, legal_moves)

            if chosenCard in legal_moves:
                curr_player.hand.remove(chosenCard)
                self.current_trick.append((chosenCard, self.currPlayerIndex))
                print(f'{curr_player.name} plays the {chosenCard.rank.name} of {chosenCard.suit.value}')
            else:
                print("Illegal move")
                break

        self.resolveTrick()
        

    def resolveTrick(self) -> None:

        initialSuit = self.current_trick[0][0].suit

        winner = []

        for [card, playerIndex] in self.current_trick:         
            if not winner:
                winner.append([card, playerIndex])
            else:
                if card.suit == initialSuit and card.rank.value > winner[0][0].rank.value:
                    winner.clear()
                    winner.append([card, playerIndex])
        
        self.currPlayerIndex = winner[0][1]
        self.players[self.currPlayerIndex].takenHands.append(self.current_trick.copy())
        self.previous_tricks.append(self.current_trick.copy())
        print(f'{self.players[self.currPlayerIndex].name} takes the trick with the {winner[0][0].rank.name} of {winner[0][0].suit.value}\n')

        self.hand_number += 1
        self.current_trick.clear() #clear trick

    def playRound(self):
        self.deal_hands()
        self.pass_cards()
        self.findLeader()

        while(self.hand_number < 14):
            self.playTrick()

        hand_scores = [0] * len(self.players)
        for i in range(len(self.players)):
            for trick in self.players[i].takenHands:
                for[card, playerIndex] in trick:
                    if card.suit == Suit.HEARTS:
                        hand_scores[i] += 1
                    if card.suit == Suit.SPADES and card.rank == Rank.Queen:
                        hand_scores[i] += 13
            self.players[i].takenHands.clear()

        if 26 in hand_scores:
            goat = hand_scores.index(26)
            for i in range(len(self.players)):
                if i == goat:
                    self.players[goat].score += 0
                    self.players[goat].scoreHistory.append(self.players[goat].score)
                else:
                    self.players[i].score += 26
                    self.players[i].scoreHistory.append(self.players[i].score)
        else:
            for i in range(len(self.players)):
                self.players[i].score += hand_scores[i]
                self.players[i].scoreHistory.append(self.players[i].score)
              
        print(f'\nFINAL ROUND SCORES')  
        for player in self.players:
            print(f"{player.name} has {player.score} points.")



        
                



        

        



