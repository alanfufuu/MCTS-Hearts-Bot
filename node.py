class Node: #representation of game states
    def __init__(self, state, parent = None, move = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.move = move
        self.wins = 0
        self.visits = 0

    def __repr__(self):
        return f'Node(move = {self.move}, visits = {self.visits}, wins = {self.wins})'
