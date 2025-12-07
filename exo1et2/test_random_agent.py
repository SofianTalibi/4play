from pettingzoo.classic import connect_four_v3
import random
from loguru import logger

def print_board(board_obs):
    """"
    Print the Connect 4 board in a readable format.
    board_obs : numpy array of shape (6,7,2)
    """
    rows, cols, _ = board_obs.shape
    for r in range(rows):
        line = ""
        for c in range(cols):
            cell = board_obs[r,c]
            if cell[0] == 1:
                line += "X "
            elif cell[1] == 1:
                line += "0 "
            else:
                line += ". "
        print(line)
    print()


def random_agent(observation, action_mask):
    """
    Choisit un coup au hasard
    """
    valid_actions = [i for i, m in enumerate(action_mask) if m==1]
    if not valid_actions:
        return None
    return random.choice(valid_actions)

def play_single_game(render=False, show_board=False, seed=None):
    env = connect_four_v3.env(render_mode="human" if render else None)
    if seed is not None:
        env.reset(seed=seed)
    else:
        env.reset()
    
    winner = None
    num_moves = 0

    for agent_name in env.agent_iter():
        obs, reward, terminated, truncated, info = env.last()

        if terminated or truncated:
            action = None
            if reward == 1:
                winner = agent_name
            elif reward == 0:
                winner = "draw"

        else:
            action_mask = obs["action_mask"]
            action = random_agent(obs["observation"], action_mask)
            num_moves += 1

            if show_board:
                print(f"{agent_name} a joué colonne {action}")
                print_board(obs["observation"])
        env.step(action)

    env.close()
    if winner is None:
        winner = "draw"
    return winner, num_moves

class RandomAgent:

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        if terminated or truncated:
            return None
        valid_actions = [i for i, m in enumerate(action_mask) if m==1]
        if not valid_actions:
            return None
        return random.choice(valid_actions)
    
class WeightedRandomAgent(RandomAgent):

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        if terminated or truncated:
            return None
        
        all_actions = list(range(len(action_mask)))

        weights = [1,2,3,4,3,2,1]

        valid_actions = [a for a in all_actions if action_mask[a] == 1]
        valid_weights = [weights[a] for a in valid_actions]

        if not valid_actions:
            return None
        
        logger.debug(f"Actions possibles: {actions}")
        logger.debug(f"Weights: {weights}")
        logger.info(f"Action choisi: {action}")
                
        chosen_action = random.choices(valid_actions, weights=valid_weights, k =1)[0]

def play_multiple_games(num_games=10, render=False, show_board=False):
    results = {"player_0": 0, "player_1": 0, "draw": 0}
    moves_list = []

    for i in range(1, num_games + 1):
        winner, num_moves = play_single_game(render=render, show_board=show_board, seed=i)
        results[winner] += 1
        moves_list.append(num_moves)
        print(f"Partie {i} : Gagnant = {winner}, coups joués = {num_moves} ")

    win_rates = {k: results[k] / num_games for k in results}
    average_moves = sum(moves_list) / num_games

    print("\n==== Apercu ====")
    print(f"Un nombre de {num_games} parties ont été faites")
    for key in results:
        print(f"{key}: {results[key]} victoires, taux de victoires = {win_rates[key]:.2f}")
    print(f"Nombre moyen de coups : {average_moves:.2f}")
    return results, win_rates

def main():

    env = connect_four_v3.env(render_mode="human")
    env.reset(seed = 42)
    
    print("Debute une partie entre 2 agents aléatoires")

    first_obs = env.observe(env.agents[0])["observation"]
    print_board(first_obs)

    for agent_name in env.agent_iter():
        obs, reward, terminated, truncated, info = env.last()

        if terminated or truncated:
            action = None
            if reward == 1:
                print(f"{agent_name} a gagné")
            elif reward == 0:
                print("Match nul")

        else:
            action_mask = obs["action_mask"]
            action = random_agent(obs["observation"], action_mask)
            print(f"{agent_name} a joué colonne {action}")

            print_board(obs["observation"])
        
        env.step(action)

    env.close()
    print("Match terminé")
    

    num_games = 100
    results, win_rates = play_multiple_games(num_games=num_games, render=False, show_board=False)
    
if __name__ == "__main__":
    main()