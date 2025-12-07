# Activité 1 : Comprendre le Puissance 4 et le framework Python PettingZoo

## Objectifs d'apprentissage

- Comprendre les règles du Puissance 4 et les conditions de victoire
- Apprendre comment PettingZoo représente les états du jeu
- Analyser l'espace d'observation et l'espace d'action
- Décomposer le problème en tâches algorithmiques

## Partie 1 : Règles du Puissance 4

### Tâche 1.1 : Analyse des règles du jeu

Répondez aux questions suivantes dans un fichier texte ou un document markdown :

1. Quelles sont les dimensions d'un plateau de Puissance 4 ?
6x7
2. Comment un joueur gagne-t-il la partie ?
En alignant 4 de ses jetons
3. Que se passe-t-il si le plateau est complètement rempli sans gagnant ?
Un match nul
4. Un joueur peut-il placer un pion dans une colonne qui est déjà pleine ?
Non
5. Quels sont les résultats possibles d'une partie ?
Vicoire ou match nul

### Tâche 1.2 : Analyse des conditions de victoire

Listez toutes les différentes façons dont un joueur peut gagner au Puissance 4 :

1. Dessinez un diagramme montrant les quatre motifs de victoire différents
Horizontale
x x x x
Verticale
x
x
x
x
Diagonale descendante (\)
x . . .
. x . .
. . x .
. . . x
Diagonale montante (/)
. . . x
. . x .
. x . .
x . . .
2. Pour une position donnée, combien de directions doivent être vérifiées pour une victoire ?
horizontale
verticale
diagonale \
diagonale /
3. Pour chacune de ces directions, quel est l'algorithme pour vérifier l'alignement de 4 pions ? Décrire l'algorithme sans le coder (pseudo-code)
pour chaque (dx, dy) dans directions :
    compteur = 1    # compte la case (row, col)

    # 1) aller dans le sens + (dx, dy)
    r = row + dx
    c = col + dy
    tant que (r, c) est dans le plateau ET board[r][c] == player :
        compteur += 1
        r += dx
        c += dy

    # 2) aller dans le sens - (dx, dy)
    r = row - dx
    c = col - dy
    tant que (r, c) est dans le plateau ET board[r][c] == player :
        compteur += 1
        r -= dx
        c -= dy

    si compteur >= 4 :
        retourner True

retourner False


**Indice** : Réfléchissez à la façon dont vous vérifieriez chaque position après avoir placé un pion.

## Partie 2 : Comprendre PettingZoo

### Tâche 2.1 : Lire la documentation

Lisez la [documentation PettingZoo de Puissance 4](https://pettingzoo.farama.org/environments/classic/connect_four/) et répondez à ces questions :

1. Quels sont les noms des deux agents dans l'environnement ?
player_0 and player_1
2. Que représente la variable `action` dans le code proposé par la documentation ? Quel est son type ?
Une action valide 
3. Que fait `env.agent_iter()` et `env.step(action)` ?
env.agent_iter() est un itérateur qui permet de parcourir les agents un par un, en l’ordre où ils doivent jouer
alors que env.agent_iter() est pour l'exécution de la boucle de jeu où les agents jouent l'un après l'autre dans le environnement
4. Quelles informations sont retournées par `env.last()` ?
observation, reward, termination, truncation, info
5. Quelle est la structure de l'observation retournée ?
(6,7,2)
6. Qu'est-ce qu'un "action mask" et pourquoi est-il important ?
c'est un vecteur de 0 et de 1 qui indique si un coup est possible/legal ou non, il est important pour assurer que le jeu soit respecté et se finit en une vrai victoire par une stratégie.


### Tâche 2.2 : Analyse de l'espace d'observation

Créez un script appelé `explore_observations.py` avec le code suivant :

```python
from pettingzoo.classic import connect_four_v3
import numpy as np

# TODO: Create environment
env = connect_four_v3.env()
env.reset(seed=42)

# TODO: Get first observation
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    # TODO: Print the observation structure
    print("Agent:", agent)
    print("Observation keys:", observation.keys())
    print("Observation shape:", observation['observation'].shape)
    print("Action mask:", observation['action_mask'])

    # TODO: Take a random action (column 3)
    env.step(3)
    break

env.close()
```

Répondez à ces questions :

1. Quelle est la forme du tableau d'observation ?
Il est de la forme d'une matrice 3D - (6,7,2)
2. Que représente chaque dimension ?
On a une matrice (6,7) qui représente la grille du jeu comme on connait. 
Ensuite la troisième dimension correspond au deux choix de jeton : rouge ou jaune.
3. Quelles sont les valeurs possibles dans le tableau d'observation ?
Les valeurs possibles sont 0 et 1 car chaque couche est un plan binaire.

### Tâche 2.3 : Comprendre la représentation du plateau

**Exercice** : Créez un script qui visualise l'état du plateau :

```python
from pettingzoo.classic import connect_four_v3
import numpy as np

def print_board(observation):
    """
    Print a human-readable version of the board

    observation: numpy array of shape (6, 7, 2)
        observation[:,:,0] = current player's pieces
        observation[:,:,1] = opponent's pieces
    """
    # TODO: Implement this function
    # Hint: Loop through rows and columns
    # Use symbols like 'X', 'O', and '.' for current player, opponent, and empty
    rows, cols, _ = observation.shape

    for r in range(rows):
        line = ""
        for c in range(cols):
            cell = observation[r, c]
            
            if cell[0] == 1:        # jeton du joueur courant
                line += "X "
            elif cell[1] == 1:      # jeton de l'adversaire
                line += "O "
            else:
                line += ". "        # case vide
        
        print(line)
    print()
    pass

# Test your function
env = connect_four_v3.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print(f"\nAgent: {agent}")
    print_board(observation['observation'])

    # Make a few moves to see the board change
    env.step(3)
    if agent == env.agents[0]:
        break

env.close()
```

### Tâche 2.4 : Créer une boucle de jeu simple

Pour consolider votre compréhension, créez un jeu simple où les deux joueurs jouent aléatoirement :

```python
# simple_game.py
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

input("Press Enter to close...")
env.close()
```

Exécutez ce script et observez comment la partie progresse. Ce sera la base pour vos propres agents !

## Partie 3 : Décomposition du problème

### Tâche 3.1 : Décomposer l'implémentation de l'agent

Un agent doit choisir quelle colonne jouer. Décomposez cela en sous-tâches :

1. **Analyse des entrées** : Quelles informations l'agent reçoit-il ?
L'agent recoit les informations suivantes :
observation, reward, termination, truncation, info = env.last()
2. **Détection des coups valides** : Comment déterminez-vous quelles colonnes sont jouables ?
avec mask = observation["action_mask"]
3. **Sélection du coup** : Quel algorithme utiliserez-vous pour choisir un coup ?
On pourrait toujours jouer au centre si possible avec :
mask = observation["action_mask"]
valid_moves = [i for i, m in enumerate(mask) if m == 1]
if 3 in valid_moves:
    action = 3
else:
    action = valid_moves[0]  
4. **Sortie** : Que doit retourner l'agent ?
Un entier entre 0 et 6 ou None si la partie est terminée.

Créez un document avec vos réponses.

### Tâche 3.2 : Conception d'algorithme - Progression

A votre avis, quels seraients les algorithmes à implémenter dans les agents (différentes stratégies de jeu), par ordre de complexité croissante :

1. **Niveau 0** : _____ (Agent le plus simple possible)
Agent complètement aléatoire, qui fait même des coups invalides
2. **Niveau 1** : _____ (Légèrement plus intelligent - éviter les coups invalides)
Agent aléatoire mais qui évite les coups invalides
3. **Niveau 2** : _____ (Chercher des opportunités immédiates)
Un agent qui cherche s'il y a un coup gagnant et si oui le prends.
Il 'cherche' en simulant le coup pour voir si ca mène à une victoire, sinon il joue aléatoirement. 
4. **Niveau 3** : _____ (Jeu défensif)
Verifie si l'adversaire peut gagner et si oui bloque ce coup.
5. **Niveau 4** : _____ (Positionnement stratégique)
Toujours jouer colonne 3 (centre) si possible. Essayer de faire 2 alignements possible.
6. **Niveau 5+** : _____ (Algorithmes avancés)
Minimax, Monte-Carlo Tree Search, Reinforcement Learning.

**Objectif** : Vous devriez avoir une progression de "aléatoire" à "expert". Cela guidera votre implémentation dans les exercices suivants.

### Tâche 3.3 : Définir l'interface de l'agent

Dans la suite, l'objectif est d'implémenter des agents selon les stratégies décrites ci-dessus. Chaque agent doit ainsi choisir une action en fonction de l'état du jeu (c-à-d la position des jetons). L'idée est d'implémenterez une classe `Agent` par stratégie.

Quel serait le squelette de cette classe (attributs, méthodes, etc.) ?

class Agent:
    def __init__(self, name="Agent"):
        """
        Initialise un agent générique.
        Paramètres :
        - name : nom de l’agent (utile pour les logs et le debug)
        """
        self.name = name

    def reset(self):
        """
        Réinitialise l’état interne de l’agent (si nécessaire).
        Appelé au début d’une nouvelle partie.
        """
        pass

    def select_action(self, observation, action_mask):
        """
        Choisit et retourne une action en fonction :
        - de l'observation (plateau, dernier coup, etc.)
        - d'un masque indiquant les actions valides
        Cette méthode DOIT être redéfinie dans les classes filles.
        Retour :
        - Un entier représentant la colonne à jouer.
        """
        raise NotImplementedError("select_action must be implemented in subclasses")


## Livrables

À la fin de cet exercice, vous devriez avoir :

1. ✅ Un document `README.md` répondant à toutes les questions sur les règles du jeu et les conditions de victoire
2. ✅ Un script (`explore_observations.py`) qui explore l'espace d'observation
3. ✅ Une fonction `print_board()` qui visualise l'état du jeu
4. ✅ Un texte de décomposition du problème avec votre plan de progression d'agent
5. ✅ Un squelette de classe d'agent avec des méthodes documentées

## Questions d'auto-vérification

Avant de passer à l'exercice 2, assurez-vous de pouvoir répondre :

1. Comment le plateau est-il représenté dans l'observation de PettingZoo ?
Par un tableau numpy 3D de dimensions (6,7,2)
2. Quel est l'espace d'action pour le Puissance 4 ?
Un entier entre 0 et 6 représentant la colonne où jouer, donc 
env.action_space(agent).n = 7
3. Comment déterminez-vous si une colonne est jouable ?
Si sa case du haut est vide:
Dans la masque fournie par l'environnement:
action_mask = observation["action_mask"] 
action_mask[i] == 1 si colonne est jouable, ==0 si pleine

4. Quelles sont les quatre directions à vérifier pour une victoire ?
Horizontale - gauche : droite
Verticale - haut : bas
Diagonale Montante - bas-gauche : haut-droite
Diagonale Descendante - haut-gauche : bas-droite
5. Quelles informations un agent reçoit-il lorsqu'il est temps de faire un coup ?
Un dictionnaire pour l'observation
Un reward 
termination/truncation - la partie est-elle terminée

## Prochaines étapes

Une fois que vous comprenez le problème et le framework, passez à :
- [Exercice 2 : Implémenter un agent aléatoire](./exercise_02_random_agent.md)

## Ressources supplémentaires

- [Documentation PettingZoo de Puissance 4](https://pettingzoo.farama.org/environments/classic/connect_four/)
- [Indexation de tableaux NumPy](https://numpy.org/doc/stable/user/basics.indexing.html)

## Conseils

- **Visualisez** : Dessiner le plateau sur papier aide à comprendre le système de coordonnées
- **Expérimentez** : Exécutez le code plusieurs fois et observez différents états de jeu
- **Demandez "Pourquoi ?"** : Comprendre les décisions de conception dans PettingZoo vous aidera plus tard
- **Documentez** : Notez votre compréhension - ce sera utile pour l'implémentation
