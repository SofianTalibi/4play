# test_smart_agent.py
# Fichier de tests propre, clair et bien organisé
# Tests unitaires + simulations + tournoi SmartAgent vs RandomAgent

import numpy as np
import random as _random
from smart_agent import SmartAgent
from loguru import logger as _logger

ROWS, COLS, CHANNELS = 6, 7, 2

# ==========================================================
# TEST 1 — _get_valid_actions
# ==========================================================
def test_get_valid_actions():
    agent = SmartAgent(env=None)

    mask_all = [1, 1, 1, 1, 1, 1, 1]
    mask_some = [0, 1, 0, 1, 0, 1, 0]

    assert agent._get_valid_actions(mask_all) == [0, 1, 2, 3, 4, 5, 6]
    assert agent._get_valid_actions(mask_some) == [1, 3, 5]

    print("Test _get_valid_actions: Passed")

# ==========================================================
# TEST 2 — _get_next_row
# ==========================================================
def test_get_next_row():
    agent = SmartAgent(env=None)
    board = np.zeros((ROWS, COLS, CHANNELS))

    # Colonne vide → tombe en bas
    assert agent._get_next_row(board, 3) == 5

    # Colonne partiellement remplie
    board[5, 3, 0] = 1
    assert agent._get_next_row(board, 3) == 4

    # Colonne pleine
    board[:, 0, 0] = 1
    assert agent._get_next_row(board, 0) is None

    print("Test _get_next_row: Passed")

# ==========================================================
# TEST 3 — _check_win_from_position
# ==========================================================
def test_check_win_from_position():
    agent = SmartAgent(env=None)
    board = np.zeros((ROWS, COLS, CHANNELS))

    # Horizontal
    board[5, 0:3, 0] = 1
    assert agent._check_win_from_position(board, 5, 3, 0) is True

    # Vertical
    board.fill(0)
    board[2:5, 1, 0] = 1
    assert agent._check_win_from_position(board, 5, 1, 0) is True

    # Diagonale /
    board.fill(0)
    board[5, 0, 0] = board[4, 1, 0] = board[3, 2, 0] = 1
    assert agent._check_win_from_position(board, 2, 3, 0) is True

    # Diagonale \
    board.fill(0)
    board[2, 0, 0] = board[3, 1, 0] = board[4, 2, 0] = 1
    assert agent._check_win_from_position(board, 5, 3, 0) is True

    # Aucun alignement
    board.fill(0)
    assert agent._check_win_from_position(board, 5, 3, 0) is False

    print("Test _check_win_from_position: Passed")

# ==========================================================
# TEST 4 — _find_winning_move
# ==========================================================
def test_find_winning_move():
    agent = SmartAgent(env=None)
    board = np.zeros((ROWS, COLS, CHANNELS))

    board[5, 0:3, 0] = 1
    valid_cols = [0, 1, 2, 3, 4, 5, 6]
    assert agent._find_winning_move(board, valid_cols, 0) == 3

    print("Test _find_winning_move: Passed")

# ==========================================================
# TEST 5 — _creates_double_threat
# ==========================================================
def test_creates_double_threat():
    agent = SmartAgent(env=None)
    board = np.zeros((ROWS, COLS, CHANNELS), dtype=int)

    # Config : jouer en colonne 3 crée une double menace
    board[5, 2, 0] = board[5, 3, 0] = board[5, 4, 0] = 1
    assert agent._creates_double_threat(board, 3, 0) is True

    print("Test _creates_double_threat: Passed")

# ==========================================================
# FONCTIONS UTILES POUR SIMULATION
# ==========================================================
def print_board(board):
    display_board = np.zeros((ROWS, COLS), dtype=int)
    display_board += board[:, :, 0]
    display_board += board[:, :, 1] * 2
    print(display_board)
    print('0 1 2 3 4 5 6')

def is_full(board):
    return all(board[0, c, 0] != 0 or board[0, c, 1] != 0 for c in range(COLS))

def simulate_game(agent1, agent2, max_moves=42):
    board = np.zeros((ROWS, COLS, CHANNELS), dtype=int)
    turn = 0
    winner = None

    while not is_full(board) and turn < max_moves and winner is None:
        current_agent = agent1 if turn % 2 == 0 else agent2
        channel = 0 if turn % 2 == 0 else 1
        action_mask = [(1 if board[0, c, 0] == 0 and board[0, c, 1] == 0 else 0) for c in range(COLS)]
        action = current_agent.choose_action(board.copy(), action_mask=action_mask)
        row = current_agent._get_next_row(board, action)
        board[row, action, channel] = 1
        if hasattr(current_agent, '_check_win_from_position'):
            if current_agent._check_win_from_position(board, row, action, channel):
                winner = current_agent.player_name
        turn += 1

    return winner

# ==========================================================
# SIMULATION DE PARTIE ENTRE DEUX SMARTAGENT
# ==========================================================
def example_smartagent_vs_smartagent():
    agent1 = SmartAgent(env=None, player_name='Agent1')
    agent2 = SmartAgent(env=None, player_name='Agent2')
    board = np.zeros((ROWS, COLS, CHANNELS), dtype=int)
    turn = 0
    winner = None

    print('--- Exemple : partie complète SmartAgent vs SmartAgent ---')
    while not is_full(board) and winner is None:
        current_agent = agent1 if turn % 2 == 0 else agent2
        channel = 0 if turn % 2 == 0 else 1
        action_mask = [(1 if board[0, c, 0] == 0 and board[0, c, 1] == 0 else 0) for c in range(COLS)]
        action = current_agent.choose_action(board.copy(), action_mask=action_mask)
        row = current_agent._get_next_row(board, action)
        board[row, action, channel] = 1
        print(f"{current_agent.player_name} joue en colonne {action}")
        print_board(board)
        if current_agent._check_win_from_position(board, row, action, channel):
            winner = current_agent.player_name
        turn += 1

    if winner:
        print(f"{winner} a gagné la partie !")
    else:
        print('Match nul !')

# ==========================================================
# TOURNOI SMARTAGENT VS RANDOMAGENT
# ==========================================================
class RandomAgent:
    def __init__(self, player_name='RandomAgent'):
        self.player_name = player_name
    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]
        return _random.choice(valid_actions)
    def _get_next_row(self, board, col):
        for row in range(ROWS-1, -1, -1):
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row
        return None

def tournament_smart_vs_random(num_games=100):
    agent_smart = SmartAgent(env=None, player_name='SmartAgent')
    agent_random = RandomAgent()
    smart_wins = 0
    random_wins = 0
    draws = 0

    for _ in range(num_games):
        winner = simulate_game(agent_smart, agent_random)
        if winner == 'SmartAgent':
            smart_wins += 1
        elif winner == 'RandomAgent':
            random_wins += 1
        else:
            draws += 1

    print(f"\nSur {num_games} parties :")
    print(f"SmartAgent a gagné {smart_wins} fois")
    print(f"RandomAgent a gagné {random_wins} fois")
    print(f"Matchs nuls: {draws}")

# ==========================================================
# LANCEMENT DE TOUS LES TESTS ET EXEMPLES
# ==========================================================
if __name__ == "__main__":
    # Tests unitaires
    test_get_valid_actions()
    test_get_next_row()
    test_check_win_from_position()
    test_find_winning_move()
    test_creates_double_threat()
    print("\nTous les tests unitaires SmartAgent sont passés !\n")

    # Simulation partie complète
    example_smartagent_vs_smartagent()

    # Tournoi SmartAgent vs RandomAgent
    tournament_smart_vs_random(num_games=100)
