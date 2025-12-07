import random
from loguru import logger
import numpy as np

class RandomAgent:
    def __init__(self, player_name="RandomAgent"):
        self.player_name = player_name

    def _get_valid_actions(self, action_mask):
        """Retourne les colonnes jouables à partir du masque d’action."""
        return [i for i, valid in enumerate(action_mask) if valid == 1]

    def _get_next_row(self, board, col):
        """Trouver la prochaine ligne libre dans la colonne."""
        for row in range(5, -1, -1):
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row
        return None

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """Choisit un coup au hasard parmi les actions valides."""
        if action_mask is None:
            raise ValueError("RandomAgent requires an action_mask to select valid actions.")

        valid_actions = self._get_valid_actions(action_mask)

        if not valid_actions:
            action = 0  # Aucun coup possible, par convention
        else:
            action = random.choice(valid_actions)

        logger.debug(f"{self.player_name}: RANDOM -> column {action}")
        return action
