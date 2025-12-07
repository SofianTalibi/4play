from tournament import run_tournament
from smart_agent import SmartAgent
from minimax_agent import MinimaxAgent

# Créer les instances
agents_dict = {
    "SmartAgent": SmartAgent(env=None, player_name="SmartAgent"),
    "MinimaxAgent": MinimaxAgent(env=None, player_name="MinimaxAgent")
}

# Lancer le tournoi
results = run_tournament(agents_dict, games_per_match=10)
