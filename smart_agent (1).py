"""
My Smart Agent for Connect Four

This agent uses rule-based heuristics to play strategically.
"""

import random
from loguru import logger

class SmartAgent:
    """
    A rule-based agent that plays strategically
    """

    def __init__(self, env, player_name=None):
        """
        Initialize the smart agent

        Parameters:
            env: PettingZoo environment
            player_name: Optional name for the agent
        """
        self.env = env
        self.player_name = player_name or "SmartAgent"
        if env is not None:
            self.action_space = env.action_space(env.agents[0])

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose an action using rule-based strategy
    
        Strategy priority:
        1. Win if possible
        2. Block opponent from winning
        3. Create double threat
        4. Play center if available
        5. Random valid move
        """
        board = observation  # uniformiser le nom
        # Get valid actions
        valid_actions = self._get_valid_actions(action_mask)
    
        # Rule 1: Try to win
        winning_move = self._find_winning_move(board, valid_actions, channel=0)
        if winning_move is not None:
            logger.success(f"{self.player_name}: COUP GAGNANT -> colonne {winning_move}")
            return winning_move
    
        # Rule 2: Block opponent
        blocking_move = self._find_winning_move(board, valid_actions, channel=1)
        if blocking_move is not None:
            logger.warning(f"{self.player_name}: BLOQUER ADVERSAIRE -> colonne {blocking_move}")
            return blocking_move
    
        # Rule 3: Avoid giving opponent a double threat
        safe_actions = [col for col in valid_actions if not self._creates_double_threat(board, col, channel=1)]
        if not safe_actions:
            safe_actions = valid_actions
    
        # Rule 4: Create double threat for self
        for col in safe_actions:
            if self._creates_double_threat(board, col, channel=0):
                logger.success(f"{self.player_name}: DOUBLE THREAT -> colonne {col}")
                return col
    
        # Rule 5: Center preference
        center_preference = [3, 2, 4, 1, 5, 0, 6]
        for col in center_preference:
            if col in safe_actions:
                logger.info(f"{self.player_name}: PRÉFÉRENCE CENTRE -> colonne {col}")
                return col
    
        # Rule 6: Random fallback
        action = random.choice(safe_actions)
        logger.debug(f"{self.player_name}: COUP ALÉATOIRE -> colonne {action}")
        return action

    def _get_valid_actions(self, action_mask):
        """
        Get list of valid column indices

        Parameters:
            action_mask: numpy array (7,) with 1 for valid, 0 for invalid

        Returns:
            list of valid column indices
        """
        valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]
        return valid_actions

    def _find_winning_move(self, board, valid_actions, channel):
        """
        Find a move that creates 4 in a row for the specified player

        Parameters:
            board: numpy array (6, 7, 2) - current board state
            valid_actions: list of valid column indices
            channel: 0 for current player, 1 for opponent

        Returns:
            column index (int) if winning move found, None otherwise
        """
        for col in valid_actions:
            row = self._get_next_row(board, col)
            if row is not None:
                # Simuler le coup
                board[row, col, channel] = 1
                if self._check_win_from_position(board, row, col, channel):
                    board[row, col, channel] = 0  # annuler la simulation
                    return col
                board[row, col, channel] = 0  # annuler la simulation
        return None

    def _get_next_row(self, board, col):
        """
        Find which row a piece would land in if dropped in column col

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

    def _check_win_from_position(self, board, row, col, channel):
        """
        Check if placing a piece at (row, col) would create 4 in a row

        Parameters:
            board: numpy array (6, 7, 2)
            row: row index (0-5)
            col: column index (0-6)
            channel: 0 or 1 (which player's pieces to check)

        Returns:
            True if this position creates 4 in a row/col/diag, False otherwise
        """
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # horizontal, vertical, diag \, diag /

        for dr, dc in directions:
            count = 1  # on compte le pion placé

            # Vérifier dans le sens positif
            r, c = row + dr, col + dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r, c, channel] == 1:
                count += 1
                r += dr
                c += dc

            # Vérifier dans le sens négatif
            r, c = row - dr, col - dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r, c, channel] == 1:
                count += 1
                r -= dr
                c -= dc

            if count >= 4:
                return True

        return False

    def _creates_double_threat(self, board, col, channel):
        """
        Check if playing column col creates two or more separate winning threats
    
        Returns:
            True if move creates double threat, False otherwise
        """
        row = self._get_next_row(board, col)
        if row is None:
            return False  # colonne pleine, pas de coup possible
    
        # Simuler le coup
        board[row, col, channel] = 1
        threat_count = 0
    
        # Vérifier pour chaque colonne si elle peut être un coup gagnant au prochain tour
        for next_col in range(board.shape[1]):
            next_row = self._get_next_row(board, next_col)
            if next_row is not None:
                board[next_row, next_col, channel] = 1
                if self._check_win_from_position(board, next_row, next_col, channel):
                    threat_count += 1
                board[next_row, next_col, channel] = 0  # annuler simulation
    
        # Annuler le coup simulé
        board[row, col, channel] = 0
    
        return threat_count >= 2

    def evaluate_position(self, board, player_channel):
        """
        Évalue le plateau pour le joueur donné
        """
        ROWS, COLS = 6, 7
        score = 0
        opponent_channel = 1 - player_channel

        def has_won(b, channel):
            for r in range(ROWS):
                for c in range(COLS):
                    if self._check_win_from_position(b, r, c, channel):
                        return True
            return False

        if has_won(board, player_channel):
            return 10000
        if has_won(board, opponent_channel):
            return -10000

        def count_n_in_row(b, channel, n):
            count = 0
            directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
            for r in range(ROWS):
                for c in range(COLS):
                    for dr, dc in directions:
                        in_row = 0
                        blocked = False
                        for k in range(n):
                            rr = r + dr*k
                            cc = c + dc*k
                            if rr < 0 or rr >= ROWS or cc < 0 or cc >= COLS:
                                blocked = True
                                break
                            if b[rr, cc, channel] == 1:
                                in_row += 1
                            elif b[rr, cc, 1-channel] == 1:
                                blocked = True
                                break
                        if not blocked and in_row == n:
                            count += 1
            return count

        score += count_n_in_row(board, player_channel, 3) * 5
        score += count_n_in_row(board, player_channel, 2) * 2
        score -= count_n_in_row(board, opponent_channel, 3) * 4
        score -= count_n_in_row(board, opponent_channel, 2) * 1

        # Centre
        center_col = COLS // 2
        for r in range(ROWS):
            if board[r, center_col, player_channel] == 1:
                score += 3

        # Pièces connectées horizontalement
        for r in range(ROWS):
            for c in range(COLS-1):
                if board[r, c, player_channel] == 1 and board[r, c+1, player_channel] == 1:
                    score += 1

        return score
