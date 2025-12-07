"""
My Minimax Agent for Connect Four

This agent uses the Minimax algorithm with alpha-beta pruning
and optimized win checking for speed.
"""

import numpy as np
import random

ROWS = 6
COLS = 7

# Réutilisation des fonctions optimisées du SmartAgent
def check_horizontal_wins(board, channel):
    for row in range(ROWS):
        row_slice = board[row, :, channel]
        for col in range(COLS - 3):
            if np.sum(row_slice[col:col+4]) == 4:
                return True
    return False

def check_vertical_wins(board, channel):
    for col in range(COLS):
        col_slice = board[:, col, channel]
        for row in range(ROWS - 3):
            if np.sum(col_slice[row:row+4]) == 4:
                return True
    return False

def check_diagonal_down(board, channel):
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if np.sum([board[row+i, col+i, channel] for i in range(4)]) == 4:
                return True
    return False

def check_diagonal_up(board, channel):
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if np.sum([board[row-i, col+i, channel] for i in range(4)]) == 4:
                return True
    return False

def check_win_optimized(board, channel):
    return (
        check_horizontal_wins(board, channel) or
        check_vertical_wins(board, channel) or
        check_diagonal_down(board, channel) or
        check_diagonal_up(board, channel)
    )

# ============================================================

class MinimaxAgent:
    """
    Minimax Agent with alpha-beta pruning and optimized win check
    """
    def __init__(self, env=None, depth=3, player_name=None):
        self.env = env
        self.depth = depth
        self.player_name = player_name or "MinimaxAgent"
        if env is not None:
            self.action_space = env.action_space(env.agents[0])

    def choose_action(self, board, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]
        best_score = -np.inf
        best_action = random.choice(valid_actions)
        for action in valid_actions:
            row = self._get_next_row(board, action)
            if row is not None:
                board[row, action, 0] = 1  # Simulate move
                score = self._minimax(board, self.depth-1, False, -np.inf, np.inf)
                board[row, action, 0] = 0
                if score > best_score:
                    best_score = score
                    best_action = action
        return best_action

    def _minimax(self, board, depth, maximizing, alpha, beta):
        if depth == 0 or check_win_optimized(board, 0) or check_win_optimized(board, 1):
            return self.evaluate_position(board, 0)
        valid_actions = [c for c in range(COLS) if self._get_next_row(board, c) is not None]
        if maximizing:
            max_eval = -np.inf
            for action in valid_actions:
                row = self._get_next_row(board, action)
                board[row, action, 0] = 1
                eval = self._minimax(board, depth-1, False, alpha, beta)
                board[row, action, 0] = 0
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = np.inf
            for action in valid_actions:
                row = self._get_next_row(board, action)
                board[row, action, 1] = 1
                eval = self._minimax(board, depth-1, True, alpha, beta)
                board[row, action, 1] = 0
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def _get_next_row(self, board, col):
        for row in range(5, -1, -1):
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row
        return None

    def evaluate_position(self, board, player_channel):
        # On peut réutiliser la fonction evaluate_position du SmartAgent
        return 0  # simplifié ici, à compléter comme dans SmartAgent
