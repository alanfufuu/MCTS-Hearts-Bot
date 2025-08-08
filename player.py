import random
import copy
import time
import math
from card import Card, Rank, Suit
from node import Node

class Player: #random bot
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []
        self.takenHands = []


    def cardsToPass(self, gameState):
        return self.hand[0:3]
    
    def cardToPlay(self, gameState, legalMoves):
        return random.choice(legalMoves)
    
class humanPlayer(Player): #human player
    def __init__(self, name):
        super().__init__(name)

    def cardsToPass(self, gameState):
        cards_to_pass = []
        print(f"{self.name}'s turn to pass cards")

        while len(cards_to_pass) != 3:
            try:
                print(f'Please choose three cards from your hand to pass {gameState.pass_direction_print}: e.g "2H, 10S, KC"')
                print([str(card) for card in self.hand])
                chosen_cards = input()

                s_chosen_cards = [s.strip().upper() for s in chosen_cards.split(",")]

                for s_card in s_chosen_cards:
                    card = Card.from_string(s_card)
                    if card:
                        cards_to_pass.append(card)
                    else:
                        print(f"Card {card} not found or is invalid. Please try again")
                        cards_to_pass = []
                        break
                if len(cards_to_pass) == 3:
                    return cards_to_pass

            except Exception as e:
                print(f'An error occured: {e}. Please try again')
                cards_to_pass = []

    def cardToPlay(self, gameState, legalMoves):
        print(f"{self.name}'s turn to play: ")
        print(f"Current trick: {gameState.current_trick}")
        print(f"Your hand: {self.hand}")
        print(f"Legal cards to play: {legalMoves}")

        chosen_card = None
        while chosen_card is None:
            try:
                user_input = input("Please choose a card to play: (e.g '2H, 10S, KC)").strip().upper()
                
                user_card = Card.from_string(user_input)

                if user_card is None:
                    print(f"Error: Card '{user_input}' is not in your hand. Please try again.")
                    continue
                
                if user_card not in legalMoves:
                    print(f"Error: You cannot play {user_input}. You must follow suit or play a valid card.")
                    continue                

                chosen_card = user_card

            except Exception as e:
                print(f"An error occurred: {e}. Please try again.")
        return chosen_card




class MCTSPlayer(Player): #mcts ai
    def __init__(self, name):
        super().__init__(name)
        self.root_node = None
        self.iteration_limit = 10000
        self.time_limit = 2
        self.knowledge = {}  # wins, visits, patterns = [winrate, hand number, hearts broken]
        self.previous_moves = [] # move, current game state, round number, hand number
        self.round_knowledge = {}

    def hash_state(self, state): #simple comparison of gamestates
        try:
            curr_hand = tuple(sorted(tuple((card.suit.value, card.rank.value)) for card in state.players[state.currPlayerIndex].hand))
            curr_trick = tuple(sorted(tuple((card.suit.value, card.rank.value)) for card, _ in state.current_trick))
            curr_scores = tuple(p.score for p in state.players)
            hand_count = tuple(len(p.hand) for p in state.players)
            game_variables = (state.hearts_broken, state.hand_number, len(state.previous_tricks), state.round_number % 4)
            return hash((curr_hand, curr_trick, curr_scores, hand_count, game_variables))
        except Exception as e:
            print("hash_state failed:", e) #is hash failing?
            import traceback; traceback.print_exc()
            return hash((state.hand_number, state.round_number, state.currPlayerIndex))

    def should_reset_tree(self, gameState):
        if self.root_node is None:
            return True
        
        if gameState.hand_number == 1 and len(gameState.previous_tricks) == 0:
            return True
    
        curr_hash = self.hash_state(gameState)
        root_hash = self.hash_state(self.root_node.state)
        return curr_hash != root_hash
        
    def update_knowledge(self):
        if not self.root_node:
            return
        
        def get_patterns(node, depth = 0):
            if depth > 3:
                return

            if node.visits > 10:
                try:
                    state_hash = self.hash_state(node.state)
                    if node.move:
                        winrate = node.wins/node.visits if node.visits > 0 else 0
                        key = (state_hash, node.move)

                        if key not in self.knowledge:
                            self.knowledge[key] = {'visits' : 0, 'wins' : 0, 'patterns' : []}

                        self.knowledge[key]['visits'] += node.visits
                        self.knowledge[key]['wins'] += node.wins
                        self.knowledge[key]['patterns'].append({
                            'winrate' : winrate,
                            'hand_number' : node.state.hand_number,
                            'hearts_broken' : node.state.hearts_broken
                        })
                except:
                    pass
            
            for child in node.children:
                get_patterns(child, depth + 1)
        
        get_patterns(self.root_node)

    def cardToPlay(self, gameState, legalMoves):
        self.clean_knowledge()

        if self.should_reset_tree(gameState): 
            if self.root_node:
                self.update_knowledge()
            self.root_node = Node(copy.deepcopy(gameState))
            print(f'Reset tree')

        startTime = time.time()
        iterations = 0

        while(time.time() - startTime) < self.time_limit and iterations < self.iteration_limit:
            try:
                selected_node = self.select(self.root_node)
                expanded_node = self.expand(selected_node)
                result = self.simulate(expanded_node)
                self.backpropogate(expanded_node, result)
                iterations += 1
            except Exception as e:
                print(f'Iteration failed: {e}')
                break
        
        print(f'{self.name} ran {iterations} iterations in {self.time_limit} seconds.')

        if not self.root_node.children:
            return random.choice(legalMoves)
        
        best_child = max(self.root_node.children, key=lambda c: c.visits)
        best_child.parent = None
        self.root_node = best_child

        self.previous_moves.append({
            'move' : best_child.move,
            'gameState' : self.hash_state(gameState)
        })

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

        try:
            state_hash = self.hash_state(node.state)
            key = (state_hash, selected_move)
            if key in self.knowledge:
                knowledge = self.knowledge[key]
                visits = min(5, knowledge['visits'] // 10)
                wins = visits * knowledge['wins'] // knowledge['visits'] if knowledge['visits'] > 0 else 0
                
                new_node.visits = visits
                new_node.wins = wins
        except:
            pass

        node.children.append(new_node)
        return new_node

    def simulate(self, node):
        new_sim = copy.deepcopy(node.state)
        numPlayers = len(new_sim.players)

        move_limit = 50
        moves = 0

        while not new_sim.is_terminal() and moves < move_limit:
            try:
                legal_moves = new_sim.legal_moves()
                if legal_moves:
                    chosenCard = random.choice(legal_moves)
                    new_sim.make_move_helper(chosenCard)
                    moves += 1
                    
                    if len(new_sim.current_trick) == numPlayers:
                        new_sim.resolveTrick()
            except Exception:
                break
            
        
        hand_scores = [0] * len(new_sim.players)
        for i, players in enumerate(new_sim.players):
            for trick in players.takenHands:
                for card, _ in trick:
                    if card.suit == Suit.Hearts:
                        hand_scores[i] += 1
                    if card.suit == Suit.Spades and card.rank == Rank.Queen:
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
        win_here = (scores[mcts_index] == min_score)



        while node is not None:
            node.visits += 1
            if win_here:
                node.wins += 1
            try:
                if node.move is not None: #no root move
                    hash = self.hash_state(node.parent.state) if node.parent else None
                    if hash is not None:
                        key = (hash, node.move)
                        if key not in self.knowledge:
                            self.knowledge[key] = {
                                'visits' : 0,
                                'wins' : 0,
                                'patterns' : []
                            }
                        self.knowledge[key]['visits'] += 1
                        if win_here:
                            self.knowledge[key]['wins'] += 1
            except Exception:
                pass

            node = node.parent

    def clean_knowledge(self):
        if len(self.knowledge) > 10000:
            to_delete = [k for k, v in self.knowledge.items() if v['visits'] < 3]
            for k in to_delete[:1000]:
                del self.knowledge[k]

            print(f'Cleaned up to {len(to_delete)} old knowledge entries of tree')

    def cardsToPass(self, gameState):
        if gameState.pass_direction == 0:
            return []
        
        cards_to_pass = []
        want_to_pass = []
        want_to_keep = []

        for card in self.hand:
            if (card.suit == Suit.Hearts and card.rank.value >= 10) or (card.suit == Suit.Spades and card.rank.value >= 10):
                want_to_pass.append(card)
            else:
                want_to_keep.append(card)
        
        #sort cards
        want_to_pass.sort(key=lambda c: (c.suit == Suit.Spades and c.rank == Rank.Queen, c.suit == Suit.Hearts, c.rank.value))
        want_to_keep.sort(key=lambda c: c.rank.value, reverse = True)

        cards_to_pass.extend(want_to_pass[:3])
        if len(cards_to_pass) < 3:
            cards_to_pass.extend(want_to_keep[: 3 - len(want_to_pass)])

        return cards_to_pass





