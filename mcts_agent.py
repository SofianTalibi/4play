"""
My MCTS Agent for Connect Four

Monte Carlo Tree Search with optimized win checking.
"""

import numpy as np
import random
import time

ROWS = 6
COLS = 7

# On réutilise les mêmes fonctions check_win_optimized et dérivées

class MCTSNode:
    def __init__(self, board, player, parent=None, move=None):
        self.board = board
        self.player = player
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        valid_moves = [c for c in range(COLS) if self._get_next_row(c) is not None]
        return len(self.children) == len(valid_moves)

    def best_child(self, c=1.41):
        scores = [(child.wins/child.visits) + c * np.sqrt(np.log(self.visits)/child.visits) for child in self.children]
        return self.children[np.argmax(scores)]

    def _get_next_row(self, col):
        for row in range(5, -1, -1):
            if self.board[row, col, 0] == 0 and self.board[row, col, 1] == 0:
                return row
        return None

class MCTSAgent:
    def __init__(self, env=None, time_limit=0.95, player_name=None):
        self.env = env
        self.time_limit = time_limit
        self.player_name = player_name or "MCTSAgent"

    def choose_action(self, board, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        root = MCTSNode(board.copy(), player=0)
        start_time = time.time()
        while time.time() - start_time < self.time_limit:
            node = root  # selection / expansion / simulation / backprop simplified
            # TODO: Implement full MCTS
            pass
        best = root.best_child(c=0)
        return best.move
