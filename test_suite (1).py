import numpy as np
import time
import tracemalloc
import random
from smart_agent import SmartAgent
from random_agent import RandomAgent

ROWS, COLS, CHANNELS = 6, 7, 2

# ------------------------------------------------------------------
# UTILS
# ------------------------------------------------------------------

def make_board():
    return np.zeros((ROWS, COLS, CHANNELS), dtype=int)

def play_and_get_action(agent, board):
    action_mask = [(1 if board[0, c, 0] == 0 and board[0, c, 1] == 0 else 0) for c in range(COLS)]
    return agent.choose_action(board.copy(), action_mask=action_mask)

# ------------------------------------------------------------------
# TESTS FONCTIONNELS
# ------------------------------------------------------------------

def test_valid_action_selection():
    board = make_board()
    agent = SmartAgent(env=None)
    action = play_and_get_action(agent, board)
    assert 0 <= action < COLS
    assert board[0, action, 0] == 0 and board[0, action, 1] == 0
    print("test_valid_action_selection: Passed")

def test_respects_action_mask():
    board = make_board()
    board[0, 3, 0] = 1  # colonne 3 bloquée
    agent = SmartAgent(env=None)
    action_mask = [1, 1, 1, 0, 1, 1, 1]
    action = agent.choose_action(board, action_mask=action_mask)
    assert action != 3
    print("test_respects_action_mask: Passed")

# ------------------------------------------------------------------
# SCÉNARIOS STRATÉGIQUES
# ------------------------------------------------------------------

def test_scenario_1_win_immediate():
    board = make_board()
    board[5, 0, 0] = 1
    board[5, 1, 0] = 1
    board[5, 2, 0] = 1
    agent = SmartAgent(env=None)
    action = play_and_get_action(agent, board)
    assert action == 3
    print("test_scenario_1_win_immediate: Passed")

def test_scenario_2_block_opponent_win():
    board = make_board()
    board[5, 0, 1] = 1
    board[5, 1, 1] = 1
    board[5, 2, 1] = 1
    agent = SmartAgent(env=None)
    action = play_and_get_action(agent, board)
    assert action == 3
    print("test_scenario_2_block_opponent_win: Passed")

def test_scenario_3_center_preference():
    board = make_board()
    agent = SmartAgent(env=None)
    action = play_and_get_action(agent, board)
    assert action == 3  # centre
    print("test_scenario_3_center_preference: Passed")

def test_scenario_4_prevent_double_threat():
    board = make_board()
    board[5, 0, 1] = 1
    board[5, 1, 0] = 1
    board[4, 1, 0] = 1
    agent = SmartAgent(env=None)
    action = play_and_get_action(agent, board)
    assert action == 3
    print("test_scenario_4_prevent_double_threat: Passed")

def test_scenario_5_avoid_losing_move():
    board = make_board()
    board[5, 0, 0] = 1
    board[4, 0, 0] = 1
    board[3, 0, 0] = 1
    board[5, 1, 1] = 1
    board[4, 1, 1] = 1
    board[3, 1, 1] = 1
    agent = SmartAgent(env=None)
    action = play_and_get_action(agent, board)
    assert action != 2
    print("test_scenario_5_avoid_losing_move: Passed")

def test_scenario_6_create_double_threat():
    board = make_board()
    board[5, 0, 0] = 1
    board[4, 1, 0] = 1
    board[3, 1, 0] = 1
    board[5, 2, 0] = 1
    agent = SmartAgent(env=None)
    action = play_and_get_action(agent, board)
    assert action == 1
    print("test_scenario_6_create_double_threat: Passed")

# ------------------------------------------------------------------
# TESTS DE PERFORMANCE
# ------------------------------------------------------------------

def test_time_per_move():
    board = make_board()
    agent = SmartAgent(env=None)
    start = time.time()
    play_and_get_action(agent, board)
    elapsed = time.time() - start
    assert elapsed < 0.1
    print(f"test_time_per_move: Passed ({elapsed:.5f}s)")

def test_memory_usage():
    board = make_board()
    agent = SmartAgent(env=None)
    tracemalloc.start()
    play_and_get_action(agent, board)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 10_000_000  # < 10 MB
    print(f"test_memory_usage: Passed (peak={peak/1e6:.2f} MB)")

# ------------------------------------------------------------------
# TESTS CONTRE AGENT ALÉATOIRE
# ------------------------------------------------------------------

def simulate_game(agent1, agent2):
    board = make_board()
    turn = 0
    while True:
        current_agent = agent1 if turn % 2 == 0 else agent2
        channel = 0 if turn % 2 == 0 else 1
        action_mask = [(1 if board[0, c, 0] == 0 and board[0, c, 1] == 0 else 0) for c in range(COLS)]
        if sum(action_mask) == 0:
            return None
        action = current_agent.choose_action(board.copy(), action_mask=action_mask)
        row = 5 - list(reversed(board[:, action, 0] + board[:, action, 1])).index(0)
        board[row, action, channel] = 1
        if hasattr(current_agent, "_check_win_from_position"):
            if current_agent._check_win_from_position(board, row, action, channel):
                return current_agent.player_name
        turn += 1

def test_smart_vs_random(num_games=10):
    smart = SmartAgent(env=None, player_name="SmartAgent")
    rnd = RandomAgent(player_name="RandomAgent")
    smart_wins = 0
    for i in range(num_games):
        winner = simulate_game(smart, rnd)
        print(f"Partie {i+1}: {winner}")
        if winner == "SmartAgent":
            smart_wins += 1
    print(f"SmartAgent a gagné {smart_wins}/{num_games} parties")
    assert smart_wins >= int(0.8 * num_games)
    print("test_smart_vs_random: Passed")

# ------------------------------------------------------------------
# MAIN — exécution de tous les tests
# ------------------------------------------------------------------

if __name__ == "__main__":
    print("=== TESTS FONCTIONNELS ===")
    test_valid_action_selection()
    test_respects_action_mask()
    print("\n=== SCÉNARIOS STRATÉGIQUES ===")
    test_scenario_1_win_immediate()
    test_scenario_2_block_opponent_win()
    test_scenario_3_center_preference()
    test_scenario_4_prevent_double_threat()
    test_scenario_5_avoid_losing_move()
    test_scenario_6_create_double_threat()
    print("\n=== TESTS DE PERFORMANCE ===")
    test_time_per_move()
    test_memory_usage()
    print("\n=== TESTS CONTRE AGENT ALÉATOIRE ===")
    test_smart_vs_random(num_games=10)
    print("\nTous les tests SmartAgent sont passés !")
