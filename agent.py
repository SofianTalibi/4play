"""
My Smart Agent for Connect Four

This agent uses rule-based heuristics to play strategically,
with optimized win checks using NumPy.
"""
# Mis sur MLARENA

import random
import numpy as np

ROWS = 6
COLS = 7

# ============================================================
#            OPTIMISATION DES VICTOIRES
# ============================================================

def check_horizontal_wins(board, channel):
    for row in range(ROWS):
        row_slice = board[row, :, channel]
        for col in range(COLS - 4 + 1):
            if np.sum(row_slice[col:col+4]) == 4:
                return True
    return False

def check_vertical_wins(board, channel):
    for col in range(COLS):
        col_slice = board[:, col, channel]
        for row in range(ROWS - 4 + 1):
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
#                     SMART AGENT
# ============================================================

class Agent:
    """
    Rule-based agent with optimized win checks
    """

    def __init__(self, env=None, player_name=None):
        self.env = env
        self.player_name = player_name or "SmartAgent"

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        board = observation
        valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]

        # 1. Win if possible
        move = self._find_winning_move(board, valid_actions, 0)
        if move is not None:
            print(f"{self.player_name}: COUP GAGNANT -> {move}")
            return move

        # 2. Block opponent
        move = self._find_winning_move(board, valid_actions, 1)
        if move is not None:
            print(f"{self.player_name}: BLOQUER ADVERSAIRE -> {move}")
            return move

        # 3. Avoid giving double threat
        safe_actions = [c for c in valid_actions if not self._creates_double_threat(board, c, 1)]
        if not safe_actions:
            safe_actions = valid_actions

        # 4. Create double threat for self
        for col in safe_actions:
            if self._creates_double_threat(board, col, 0):
                print(f"{self.player_name}: DOUBLE THREAT -> {col}")
                return col

        # 5. Center preference
        center_order = [3, 2, 4, 1, 5, 0, 6]
        for col in center_order:
            if col in safe_actions:
                print(f"{self.player_name}: CENTRE -> {col}")
                return col

        # 6. Random fallback
        action = random.choice(safe_actions)
        print(f"{self.player_name}: RANDOM -> {action}")
        return action

    def act(self, *args, **kwargs):
        return self.choose_action(*args, **kwargs)

    # -------------------------
    # Helper methods
    # -------------------------

    def _get_next_row(self, board, col):
        for row in range(5, -1, -1):
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row
        return None

    def _find_winning_move(self, board, valid_actions, channel):
        for col in valid_actions:
            row = self._get_next_row(board, col)
            if row is not None:
                board[row, col, channel] = 1
                if check_win_optimized(board, channel):
                    board[row, col, channel] = 0
                    return col
                board[row, col, channel] = 0
        return None

    def _creates_double_threat(self, board, col, channel):
        row = self._get_next_row(board, col)
        if row is None:
            return False
        board[row, col, channel] = 1
        threat_count = 0
        for next_col in range(COLS):
            next_row = self._get_next_row(board, next_col)
            if next_row is not None:
                board[next_row, next_col, channel] = 1
                if check_win_optimized(board, channel):
                    threat_count += 1
                board[next_row, next_col, channel] = 0
        board[row, col, channel] = 0
        return threat_count >= 2
