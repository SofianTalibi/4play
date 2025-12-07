# Exercice 2 : Implémenter un agent aléatoire

## Objectifs

- Implémenter un agent fonctionnel complet
- Comprendre la boucle d'interaction agent-environnement
- Utiliser les masques d'action pour garantir des coups valides
- Tester votre agent dans une vraie partie

## Introduction

L'agent le plus simple possible est celui qui choisit des coups aléatoirement. Bien que non stratégique, c'est un point de départ parfait car :

1. Il est simple à implémenter
2. Il enseigne l'interface de l'agent
3. Il fournit une référence pour la comparaison
4. Il gère tous les cas limites (colonnes pleines, fin de partie, etc.)

## Partie 1 : Implémentation

### Tâche 2.1 : Créer votre fichier d'agent

Créez un nouveau fichier appelé `random_agent.py` :

```python
"""
My Random Agent for Connect Four

This agent chooses moves randomly from the available (valid) columns.
"""

import random


class RandomAgent:
    """
    A simple agent that plays randomly
    """

    def __init__(self, env, player_name=None):
        """
        Initialize the random agent

        Parameters:
            env: PettingZoo environment
            player_name: Optional name for the agent (for display)
        """
        self.env = env
        self.player_name = player_name

        self.action_space = env.action_space(env.agents[0])
        pass

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose a random valid action

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            reward: float - reward from previous action
            terminated: bool - is the game over?
            truncated: bool - was the game truncated?
            info: dict - additional info
            action_mask: numpy array (7,) - which columns are valid (1) or full (0)

        Returns:
            action: int (0-6) - which column to play
        """
        if terminal or truncated:
            return None

        action = self.action_space.sample(mask = action_mask)
        return action
        pass  
```

### Tâche 2.2 : Compléter l'implémentation

Remplissez les TODOs dans le code ci-dessus. Voici ce que vous devez faire :

1. **Initialiser l'espace d'action** : Obtenez-le depuis l'environnement
2. **Implémenter `choose_action`** : Utilisez le masque d'action pour sélectionner un coup valide aléatoire

**Indices** :
- Voir la méthode `.sample(mask)` de l'espace d'action de PettingZoo 
- Le masque est un tableau binaire où 1 = valide, 0 = invalide

### Tâche 2.3 : Implémentation alternative (manuelle)

De façon alternative, vous pouvez implémentez une version qui n'utilise pas `.sample()` :

```python
def choose_action_manual(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
    """
    Choose a random valid action without using .sample()

    This is a learning exercise to understand what action_mask does
    """
    # TODO: Get list of valid actions from action_mask
    if terminated or truncated:
        return None
    
    valid_actions = [i for i in range(len(action_mask)) if action_mask[i] == 1]
    valid_actions = []  # Fill this list

    # TODO: If no valid actions, return None (shouldn't happen in Connect Four)
    if not valid_actions:
        return None

    # TODO: Choose randomly from valid actions
    return None  # Replace with random choice
```

## Partie 2 : Tester votre agent

L'objectif de cette partie est de tester l'agent que vous avez créé ci-dessus.
Pour cela, il vous faut implémenter un script de test, où deux agents (classe `RandomAgent` pour le moment) s'affrontent dans le jeu.

Vous pouvez vous référer au code ci-dessous en y intégrant vos objets de classe `RandomAgent`.


```python
from pettingzoo.classic import connect_four_v3

env = connect_four_v3.env(render_mode="human") # ou render_mode="rdb_array" ou bien None
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
        if reward == 1:
            print(f"{agent} wins!")
        elif reward == 0:
            print("It's a draw!")
    else:
        # Take a random valid action
        mask = observation["action_mask"]
        action = env.action_space(agent).sample(mask)
        print(f"{agent} plays column {action}")

    env.step(action)

env.close()
```


### Tâche 2.4 : Créer un script de test

Créez un programme `test_random_agent.py` qui fait jouer deux agents sur une partie.
Ce programme affiche les coups joués par les deux agents et le résultat final. De façon optionnelle, le test peut afficher l'état du plateau de jeu à chaque coup joué.


### Tâche 2.5 : Exécuter le test

```bash
python test_my_random_agent.py
```

**Ce qu'il faut observer** :
1. Le jeu s'exécute-t-il sans erreurs ?
Oui
2. L'agent fait-il des coups valides (pas d'erreurs "colonne pleine") ?
Oui
3. Le jeu se termine-t-il correctement avec un gagnant ou un match nul ?
Oui 
4. Combien de coups dure une partie typique ?
20-30 coups

### Tâche 2.6 : Tester plusieurs parties

Implémentez une fonction qui fait jouer les deux agents plusieurs fois (un entier `num_games` passé en argument). La fonction affiche et retourne les résultats comme par exemple le nombres de parties gagnées par chaque agent, taux de victoire, etc.

Ajoutez cette fonction au script `test_random_agent.py`.


## Partie 3 : Analyse

### Tâche 2.7 : Analyse statistique

Exécutez 100 parties et répondez à ces questions :

1. **Distribution des victoires** : Les victoires sont-elles à peu près égales entre le joueur 1 et le joueur 2 ?
Oui on a joueur_1 : 53 victoires et joueur_2 : 46 et un match nul
2. **Avantage du premier coup** : Le joueur 1 (qui commence) a-t-il un avantage ?
il semblerait oui, il remporte toujours plus de matchs que joueur_2
3. **Durée de la partie** : Quel est le nombre moyen de coups ? Min et max ?
20.57 moyen
9 min
35 max
4. **Fréquence des matchs nuls** : À quelle fréquence les parties se terminent-elles par un match nul ?
assez peu, une fois sur 300

Écrivez vos observations dans un fichier appelé `random_agent_analysis.md`.

### Tâche 2.8 : Liste de vérification du code

Examinez votre code par rapport à cette liste de vérification :

- [X] Votre agent gère-t-il correctement le masque d'action ?
- [X] Votre code a-t-il une documentation appropriée (docstrings) ?
- [X] Les noms de variables sont-ils clairs et descriptifs ?
- [X] L'agent fonctionne-t-il pour le joueur 1 et le joueur 2 ?
- [Peut etre] Y a-t-il des cas limites que vous n'avez pas considérés ?

## Partie 4 : Extensions (optionnel)

### Tâche 2.9 : Aléatoire pondéré

Implémentez un agent aléatoire "plus intelligent" qui préfère la colonne du centre, en utilisant l'héritage de classe.

```python
class WeightedRandomAgent(RandomAgent):
    """
    Random agent that prefers center columns
    """

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        # TODO: Create weights that favor center (column 3)
        # TODO: Filter by action_mask
        # TODO: Use random.choices(actions, weights=weights)
        actions = list(range(len(action_mask)))
        weights = [1.0] * len(actions)
        center_col = len(actions) // 2
        weights[center_col] = 3.0
        for i, allowed in enumerate(action_mask):
            if not allowed:
                weights[i] = 0.0
        return random.choices(actions, weights=weights, k=1)[0]
        

        
```

### Tâche 2.10 : Ajouter des logs

Modifiez votre agent pour afficher des logs à l'exécution, en utilisant la librairie `loguru`.

from loguru import logger

logger.debug(f"Actions possibles: {actions}")
        logger.debug(f"Weights: {weights}")
        logger.info(f"Action choisi: {action}")

## Livrables

À la fin de cet exercice, vous devriez avoir :

1. ✅ `random_agent.py` - Un agent aléatoire fonctionnel
2. ✅ `test_random_agent.py` - Script de test avec statistiques
3. ✅ `random_agent_analysis.md` - Votre analyse des résultats
4. ✅ Un code fonctionnel qui joue des parties complètes sans erreurs

## Questions d'auto-vérification

Avant de passer à l'exercice 3, assurez-vous de pouvoir répondre :

1. Pourquoi le masque d'action est-il important ?
Pour empecher des coups invalides et assurer une partie de Puissance 4 légal et utile pour l'apprentissage.
2. Que se passe-t-il si vous essayez de jouer dans une colonne pleine ?
On ne peut pas faire un tel coup grâce à action_mask
3. Comment obtenez-vous la liste des actions valides à partir du masque d'action ?
on selectionne les indices où action_mask[i] == 1 avec par exemple :
valid_actions = [i for i, v in enumerate(action_mask) if v == 1]
4. Pourquoi deux agents aléatoires pourraient-ils ne pas avoir exactement 50/50 de taux de victoire ?
Parce que le joueur qui commence la partie aura toujours un avantage structurel, en plus le hasard seul peut provoquer des écarts statistiques qui font que on n'a pas 50/50
5. Quel est le nombre maximum de coups dans une partie de Puissance 4 ?
42 coups pour remplir une grille 6x7

## Problèmes courants et solutions

### Problème : "IndexError: index out of bounds"
**Solution** : Assurez-vous que vous utilisez correctement le masque d'action. Les actions doivent être comprises entre 0 et 6.

### Problème : "L'agent joue toujours la colonne 0"
**Solution** : Vérifiez que vous utilisez effectivement une sélection aléatoire, et non simplement le retour de la première action valide.

### Problème : La partie ne se termine jamais
**Solution** : Assurez-vous de vérifier la variable de terminaison et de faire un pas avec `action=None` lorsque la partie est terminée.

## Prochaines étapes

Une fois que vous avez un agent aléatoire fonctionnel, passez à :
- [Exercice 3 : Implémenter un agent basé sur des règles](./exercise_03_rule_based_agent.md)

## Ressources supplémentaires

- [Module Random de Python](https://docs.python.org/3/library/random.html)
- [Documentation API de PettingZoo](https://pettingzoo.farama.org/api/)
