"""
Minimax Agent with alpha-beta pruning for Connect 4

This agent uses the minimax algorithm with alpha-beta pruning
to select moves strategically.
"""

import numpy as np
import random

ROWS, COLS = 6, 7  # dimensions du plateau

class MinimaxAgent:
    """
    Agent utilisant l'algorithme minimax avec élagage alpha-beta
    """

    def __init__(self, env=None, depth=4, player_name=None):
        """
        Initialisation de l'agent

        Parameters:
            env: PettingZoo environment (optionnel)
            depth: profondeur de recherche pour minimax
            player_name: nom optionnel de l'agent
        """
        self.env = env
        self.depth = depth
        self.player_name = player_name or f"Minimax(d={depth})"

    def choose_action(self, board, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choisir une action selon l'algorithme minimax avec alpha-beta

        Parameters:
            board: état actuel du plateau (numpy array 6x7x2)
            action_mask: tableau binaire indiquant les colonnes valides

        Returns:
            index de la colonne choisie (int)
        """
        valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]

        best_action = None
        best_value = float('-inf')

        # Évaluer chaque coup possible
        for action in valid_actions:
            new_board = self._simulate_move(board, action, channel=0)
            value = self._minimax(new_board, self.depth - 1, float('-inf'), float('inf'), maximizing=False)
            if value > best_value:
                best_value = value
                best_action = action

        # Retourner l'action choisie ou une colonne aléatoire si aucune
        return best_action if best_action is not None else random.choice(valid_actions)

    def _minimax(self, board, depth, alpha, beta, maximizing):
        """
        Algorithme minimax avec élagage alpha-beta

        Parameters:
            board: état actuel du plateau
            depth: profondeur restante
            alpha, beta: bornes pour l'élagage
            maximizing: True si c'est le tour du joueur maximisant (0)

        Returns:
            valeur évaluée de la position
        """
        # Condition d'arrêt: profondeur 0, victoire ou match nul
        if depth == 0 or self._check_win(board, 0) or self._check_win(board, 1) or len(self._get_valid_moves(board)) == 0:
            return self._evaluate(board)

        valid_moves = self._get_valid_moves(board)

        if maximizing:
            value = float('-inf')
            for col in valid_moves:
                new_board = self._simulate_move(board, col, 0)
                value = max(value, self._minimax(new_board, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # élagage
            return value
        else:
            value = float('inf')
            for col in valid_moves:
                new_board = self._simulate_move(board, col, 1)
                value = min(value, self._minimax(new_board, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break  # élagage
            return value

    def _simulate_move(self, board, col, channel):
        """
        Simule un coup sans modifier le plateau original

        Parameters:
            board: plateau actuel
            col: colonne où jouer
            channel: joueur (0 ou 1)

        Returns:
            nouveau plateau après le coup simulé
        """
        new_board = board.copy()
        for row in range(ROWS-1, -1, -1):
            if new_board[row, col, 0] == 0 and new_board[row, col, 1] == 0:
                new_board[row, col, channel] = 1
                break
        return new_board

    def _get_valid_moves(self, board):
        """
        Renvoie la liste des colonnes valides

        Parameters:
            board: plateau actuel

        Returns:
            liste des indices de colonnes valides
        """
        return [c for c in range(COLS) if board[0, c, 0] == 0 and board[0, c, 1] == 0]

    def _evaluate(self, board):
        """
        Évalue la position pour le joueur 0

        Parameters:
            board: plateau actuel

        Returns:
            score (int) positif si avantage joueur 0, négatif si avantage joueur 1
        """
        score = 0

        # Victoire immédiate
        if self._check_win(board, 0):
            return 10000
        if self._check_win(board, 1):
            return -10000

        # Menaces et alignements partiels
        for r in range(ROWS):
            for c in range(COLS):
                for dr, dc in [(0,1),(1,0),(1,1),(-1,1)]:
                    line = []
                    for k in range(4):
                        rr = r + dr*k
                        cc = c + dc*k
                        if 0 <= rr < ROWS and 0 <= cc < COLS:
                            if board[rr, cc, 0]:
                                line.append(1)
                            elif board[rr, cc, 1]:
                                line.append(-1)
                            else:
                                line.append(0)
                    # Points selon alignements
                    if line.count(1) == 3 and line.count(0) == 1:
                        score += 5
                    if line.count(1) == 2 and line.count(0) == 2:
                        score += 2
                    if line.count(-1) == 3 and line.count(0) == 1:
                        score -= 4
                    if line.count(-1) == 2 and line.count(0) == 2:
                        score -= 1

        # Colonne centrale
        for r in range(ROWS):
            if board[r, COLS//2, 0]:
                score += 3

        return score

    def _check_win(self, board, channel):
        """
        Vérifie si le joueur a gagné (4 alignés)

        Parameters:
            board: plateau actuel
            channel: joueur (0 ou 1)

        Returns:
            True si victoire, False sinon
        """
        for r in range(ROWS):
            for c in range(COLS):
                for dr, dc in [(0,1),(1,0),(1,1),(-1,1)]:
                    count = 0
                    for k in range(4):
                        rr = r + dr*k
                        cc = c + dc*k
                        if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr, cc, channel]:
                            count += 1
                    if count == 4:
                        return True
        return False
