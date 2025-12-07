import time
from smart_agent import SmartAgent
from minimax_agent import MinimaxAgent
import numpy as np

ROWS, COLS, CHANNELS = 6, 7, 2

def make_board():
    return np.zeros((ROWS, COLS, CHANNELS), dtype=int)

def simulate_game(agent1, agent2):
    board = make_board()
    turn = 0
    winner = None

    while True:
        current_agent = agent1 if turn % 2 == 0 else agent2
        channel = 0 if turn % 2 == 0 else 1

        # Colonnes valides
        valid_cols = [c for c in range(COLS) if board[0, c, 0] == 0 and board[0, c, 1] == 0]
        if not valid_cols:
            break  # match nul

        # Créer action_mask pour tous les agents
        action_mask = [1 if c in valid_cols else 0 for c in range(COLS)]

        # Choisir action
        action = current_agent.choose_action(board.copy(), action_mask=action_mask)

        # Placer jeton
        for row in range(ROWS-1, -1, -1):
            if board[row, action, 0] == 0 and board[row, action, 1] == 0:
                board[row, action, channel] = 1
                break

        # Vérifier victoire
        if hasattr(current_agent, "_check_win_from_position"):
            if current_agent._check_win_from_position(board, row, action, channel):
                winner = current_agent.player_name
                break

        turn += 1

    return winner


# Tâche 5.5 : tester différentes profondeurs
games_per_depth = 5  # nombre de parties pour chaque profondeur

for depth in [2, 3, 4, 5, 6]:
    minimax = MinimaxAgent(env=None, depth=depth, player_name=f"Minimax(d={depth})")
    smart = SmartAgent(env=None, player_name="SmartAgent")

    wins_minimax = 0
    wins_smart = 0
    total_time = 0

    for _ in range(games_per_depth):
        start = time.time()
        winner = simulate_game(minimax, smart)
        total_time += time.time() - start

        if winner == minimax.player_name:
            wins_minimax += 1
        elif winner == smart.player_name:
            wins_smart += 1

    avg_time = total_time / games_per_depth
    print(f"Profondeur {depth}: Minimax {wins_minimax}/{games_per_depth}, Smart {wins_smart}/{games_per_depth}, temps moyen: {avg_time:.3f}s")
