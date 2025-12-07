"""
Tournament module for Connect 4

This module allows to run a round-robin tournament between multiple agents.
It includes:
- simulate_game: simulate a single game between two agents
- run_tournament: run multiple matches between all pairs of agents
"""

import numpy as np
import random
from smart_agent import SmartAgent
from random_agent import RandomAgent
from minimax_agent import MinimaxAgent

ROWS, COLS, CHANNELS = 6, 7, 2

def get_next_row(board, col):
    """
    Find which row a piece would land in if dropped in column col.

    Parameters:
        board: numpy array (6, 7, 2)
        col: column index (0-6)

    Returns:
        row index (0-5) if space available, None if column full
    """
    for row in range(5, -1, -1):  # commencer par le bas
        if board[row, col, 0] == 0 and board[row, col, 1] == 0:
            return row
    return None  # colonne pleine

def check_win(board, channel):
    """
    Check if the given player has won (4 in a row/col/diagonal).

    Parameters:
        board: numpy array (6, 7, 2)
        channel: 0 or 1 (player index)

    Returns:
        True if player has 4 connected pieces, False otherwise
    """
    directions = [(0,1),(1,0),(1,1),(-1,1)]  # horizontal, vertical, diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r, c, channel] == 1:
                for dr, dc in directions:
                    count = 1
                    # Vérifier dans le sens positif
                    rr, cc = r+dr, c+dc
                    while 0<=rr<ROWS and 0<=cc<COLS and board[rr,cc,channel]==1:
                        count += 1
                        rr += dr
                        cc += dc
                    # Vérifier dans le sens négatif
                    rr, cc = r-dr, c-dc
                    while 0<=rr<ROWS and 0<=cc<COLS and board[rr,cc,channel]==1:
                        count += 1
                        rr -= dr
                        cc -= dc
                    if count >= 4:
                        return True
    return False

def simulate_game(agent1, agent2, verbose=False):
    """
    Simulate a single Connect 4 game between two agents.

    Parameters:
        agent1, agent2: agent instances
        verbose: whether to print moves

    Returns:
        winner's name (str) if there is a winner, None for a draw
    """
    board = np.zeros((ROWS, COLS, CHANNELS), dtype=int)
    turn = 0
    winner = None

    while True:
        current_agent = agent1 if turn % 2 == 0 else agent2
        channel = 0 if turn % 2 == 0 else 1

        # Créer le masque des colonnes valides
        action_mask = [1 if board[0, c, 0] == 0 and board[0, c, 1] == 0 else 0 for c in range(COLS)]
        if sum(action_mask) == 0:
            break  # match nul

        # Choisir l'action via l'agent
        action = current_agent.choose_action(board.copy(), action_mask=action_mask)

        # Trouver la ligne où placer le pion
        row = get_next_row(board, action)
        if row is None:
            continue  # colonne pleine, ignorer le coup
        board[row, action, channel] = 1

        if verbose:
            print(f"{current_agent.player_name} joue colonne {action}")

        # Vérifier la victoire
        if check_win(board, channel):
            winner = current_agent.player_name
            break

        turn += 1

    return winner

def run_tournament(agents_dict, games_per_match=3, verbose=False):
    """
    Run a round-robin tournament between all agents.

    Parameters:
        agents_dict: dict {agent_name: agent_instance}
        games_per_match: number of games per match
        verbose: whether to print game moves

    Returns:
        dict of scores {agent_name: points}
    """
    scores = {name: 0 for name in agents_dict.keys()}
    names = list(agents_dict.keys())

    # Chaque paire d'agents s'affronte
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            A = agents_dict[names[i]]
            B = agents_dict[names[j]]

            print(f"\n===== Match {names[i]} vs {names[j]} =====")
            for g in range(games_per_match):
                winner = simulate_game(A, B, verbose=verbose)
                if winner:
                    scores[winner] += 1

    print("\n===== Résultats finaux =====")
    for name, score in scores.items():
        print(f"{name}: {score} points")

    return scores

if __name__ == "__main__":
    # Créer les instances des agents
    agents_dict = {
        "SmartAgent": SmartAgent(env=None, player_name="SmartAgent"),
        "RandomAgent": RandomAgent(player_name="RandomAgent"),
        "MinimaxAgent": MinimaxAgent(env=None, player_name="MinimaxAgent")
    }

    # Lancer le tournoi
    run_tournament(agents_dict, games_per_match=3)
