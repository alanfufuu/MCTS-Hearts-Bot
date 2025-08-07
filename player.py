import random
import copy
import time
import math
from card import Card, Rank, Suit
from node import Node

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []
        self.takenHands = []


    def cardsToPass(self, gameState):
        return self.hand[0:3]
    
    def cardToPlay(self, gameState, legalMoves):
        return random.choice(legalMoves)
    


class MCTSPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.iteration_limit = 1000
        self.time_limit = 1

    def cardToPlay(self, gameState, legalMoves):
        root_state = copy.deepcopy(gameState)
        root_node = Node(root_state)

        startTime = time.time()
        iterations = 0

        while(time.time() - startTime) < self.time_limit:
            selected_node = self.select(root_node)
            
            expanded_node = self.expand(selected_node)

            result = self.simulate(expanded_node)

            self.backpropogate(expanded_node, result)

            iterations += 1
        
        print(f'{iterations} iterations were ran in {self.time_limit} seconds.')

        best_child = None
        max_visits = -1

        for child in root_node.children:
            if child.visits > max_visits:
                max_visits = child.visits
                best_child = child
        
        if best_child is None:
            return random.choice(legalMoves)
        
        return best_child.move
    
    def uct(self, child, parent, C = 1.414):
        if child.visits == 0:
            return float("inf")
        
        exploitation = child.wins/child.visits
        exploration = math.sqrt(math.log(parent.visits)/child.visits)

        return exploitation + C * exploration

    def select(self, node):
        while node.children:
            unvisited_children = [child for child in node.children if child.visits == 0]
            if unvisited_children:
                return random.choice(unvisited_children)
            
            uct_scores = [self.uct(child, node) for child in node.children]
            uct_max = uct_scores.index(max(uct_scores))
            node = node.children[uct_max]
        return node

    def expand(self, node):
        legal_moves = node.state.legal_moves()
        if not legal_moves:
            return node

        existing = {child.move for child in node.children}
        unexplored_moves = [move for move in legal_moves if move not in existing]
        if not unexplored_moves:
            return node
        
        selected_move = random.choice(unexplored_moves)
        
        temp_state = copy.deepcopy(node.state)
        temp_state.make_move_helper(selected_move)

        new_node = Node(state = temp_state, parent = node, move = selected_move)
        node.children.append(new_node)

        return new_node

    def simulate(self, node):
        new_sim = copy.deepcopy(node.state)
        numPlayers = len(new_sim.players)

        while not new_sim.is_terminal():
            legal_moves = new_sim.legal_moves()
            if legal_moves:
                chosenCard = random.choice(legal_moves)
                new_sim.make_move_helper(chosenCard)
                
                if len(new_sim.current_trick) == numPlayers:
                    new_sim.resolveTrick()
                
            
        
        hand_scores = [0] * len(new_sim.players)
        for i, players in enumerate(new_sim.players):
            for trick in players.takenHands:
                for card, _ in trick:
                    if card.suit == Suit.HEARTS:
                        hand_scores[i] += 1
                    if card.suit == Suit.SPADES and card.rank == Rank.Queen:
                        hand_scores[i] += 13
            new_sim.players[i].takenHands.clear()

        if 26 in hand_scores:
            goat = hand_scores.index(26)
            for i in range(len(new_sim.players)):
                if i == goat:
                    new_sim.players[goat].score += 0
                else:
                    new_sim.players[i].score += 26
        else:
            for i in range(len(new_sim.players)):
                new_sim.players[i].score += hand_scores[i]
        return hand_scores

    def backpropogate(self, node, scores) -> None:
        mcts_name = self.name
        mcts_index = -1

        for i, player in enumerate(node.state.players):
            if player.name == mcts_name:
                mcts_index = i
                break
        if mcts_index < 0:
            return
        
        min_score = min(scores)

        while node is not None:
            node.visits += 1

            if scores[mcts_index] == min_score:
                node.wins += 1

            node = node.parent
                







