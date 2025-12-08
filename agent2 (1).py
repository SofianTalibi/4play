"""
Ultra-Optimized Hybrid Smart Agent for Connect Four
Rule-based + Adaptive Minimax + Mini MCTS
Optimized for top ranking on ML-Arena
"""

import random
import numpy as np
import math

ROWS = 6
COLS = 7

# ===============================
# Vectorized Win Checks
# ===============================

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

# ===============================
# Ultra-Optimized Hybrid Agent
# ===============================

class Agent:
    def __init__(self, env, player_name=None):
        self.env = env
        self.player_name = player_name or "UltraOptHybrid"

        # Minimax & MCTS parameters
        self.minimax_depth = 3
        self.mcts_simulations = 15
        self.alpha = 0.7
        self.beta = 0.3

        if env is not None:
            self.action_space = env.action_space(env.agents[0])

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        board = observation
        valid_actions = [i for i, valid in enumerate(action_mask) if valid==1]

        # --- 1. Victory / block check ---
        for ch in [0, 1]:
            for col in valid_actions:
                row = self._get_next_row(board, col)
                if row is None:
                    continue
                board[row, col, ch] = 1
                if check_win_optimized(board, ch):
                    board[row, col, ch] = 0
                    return col
                board[row, col, ch] = 0

        # --- 2. Safe actions (no double threat) ---
        safe_actions = [c for c in valid_actions if not self._creates_double_threat(board, c, 1)]
        if not safe_actions:
            safe_actions = valid_actions

        # --- 3. Evaluate with Minimax + Mini-MCTS ---
        scores = {}
        for col in safe_actions:
            row = self._get_next_row(board, col)
            if row is None:
                continue
            board_copy = board.copy()
            board_copy[row, col, 0] = 1

            minimax_score = self._minimax(board_copy, self.minimax_depth, False, -10000, 10000)
            mcts_score = self._simulate_mcts(board, col, 5)  # only 5 short simulations for speed

            scores[col] = self.alpha * minimax_score + self.beta * mcts_score

        return max(scores, key=scores.get)

    # Alias
    def act(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        return self.choose_action(observation, reward, terminated, truncated, info, action_mask)

    # ===============================
    # Helper methods
    # ===============================
    def _get_next_row(self, board, col):
        for row in range(ROWS-1, -1, -1):
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row
        return None

    def _creates_double_threat(self, board, col, channel):
        row = self._get_next_row(board, col)
        if row is None:
            return False
        board[row, col, channel] = 1
        threat_count = 0
        for c in range(COLS):
            r = self._get_next_row(board, c)
            if r is not None:
                board[r, c, channel] = 1
                if check_win_optimized(board, channel):
                    threat_count += 1
                board[r, c, channel] = 0
        board[row, col, channel] = 0
        return threat_count >= 2

    # ===============================
    # Minimax + alpha-beta pruning
    # ===============================
    def _minimax(self, board, depth, maximizing, alpha, beta):
        if depth == 0:
            return self._evaluate_board(board)
        valid_actions = [c for c in range(COLS) if self._get_next_row(board, c) is not None]
        if maximizing:
            max_eval = -math.inf
            for col in valid_actions:
                row = self._get_next_row(board, col)
                board_copy = board.copy()
                board_copy[row, col, 0] = 1
                if check_win_optimized(board_copy, 0):
                    return 1000
                eval = self._minimax(board_copy, depth-1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for col in valid_actions:
                row = self._get_next_row(board, col)
                board_copy = board.copy()
                board_copy[row, col, 1] = 1
                if check_win_optimized(board_copy, 1):
                    return -1000
                eval = self._minimax(board_copy, depth-1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def _evaluate_board(self, board):
        score = 0
        center_col = COLS//2
        for r in range(ROWS):
            for c in range(COLS):
                if board[r, c, 0] == 1:
                    score += 3 if c == center_col else 1
                elif board[r, c, 1] == 1:
                    score -= 3 if c == center_col else 1
        return score

    # ===============================
    # Mini-MCTS simulation (short)
    # ===============================
    def _simulate_mcts(self, board, col, simulations):
        wins = 0
        for _ in range(simulations):
            board_copy = board.copy()
            row = self._get_next_row(board_copy, col)
            if row is None:
                continue
            board_copy[row, col, 0] = 1
            player = 1
            for _ in range(10):
                valid_moves = [c for c in range(COLS) if self._get_next_row(board_copy, c) is not None]
                if not valid_moves:
                    break
                move = random.choice(valid_moves)
                r = self._get_next_row(board_copy, move)
                board_copy[r, move, player] = 1
                if check_win_optimized(board_copy, player):
                    if player == 0:
                        wins += 1
                    break
                player = 1 - player
        return wins
