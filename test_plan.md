1. Introduction

Ce document présente la stratégie de test que j’ai mise en place pour vérifier le bon fonctionnement des agents développés dans les exercices précédents (RandomAgent, SmartAgent).
L’objectif est de garantir que les agents respectent les règles du jeu, qu’ils sont robustes face à différents scénarios, et qu’ils offrent un comportement cohérent et performant.

2. Catégories de tests

J’ai organisé les tests en trois grandes catégories :

Tests fonctionnels

Tests de performance

Tests stratégiques

L’idée est de couvrir à la fois la validité des actions, le comportement en conditions limites, et la qualité réelle du jeu produit par les agents.

3. Tests fonctionnels

Ces tests vérifient que les agents suivent correctement les règles du jeu.
C’est le socle minimal : un agent peut être faible stratégiquement, mais il doit au moins être correct.

3.1 Validité des actions

Objectif : s’assurer que l’action renvoyée par l’agent respecte toujours le masque fourni.

Scénarios prévus :

Masque normal (plusieurs actions possibles)

Masque avec une seule action valide

Masque rempli de zéros (aucune action possible)

Masque de taille inattendue (erreur attendue)

Masque contenant des valeurs anormales (ex. floats ou -1)

Ces tests garantissent que l’agent n’essaie jamais de jouer un coup interdit.

3.2 Gestion de la fin de partie

Cas testés :

L’agent reçoit un état terminal → il doit renvoyer soit None, soit une action neutre définie par les règles.

L’agent ne doit pas essayer de jouer plusieurs fois après une condition terminale.

Ce test permet d’éviter des comportements absurdes comme jouer après un match déjà fini.

3.3 Comportements exceptionnels

Idées de tests :

Entrées invalides (type, dimensions)

Masque vide

Appels successifs sur des états incohérents

Objectif : s’assurer que l’agent ne crash pas n’importe comment, mais réagit proprement (erreur explicite ou comportement contrôlé selon l’implémentation).

4. Tests de performance

L’idée ici est de vérifier que l’agent reste utilisable même dans un grand nombre de coups ou de parties.

4.1 Temps moyen par coup

Je mesure :

le temps moyen pour choisir une action,

le temps maximal,

la stabilité du temps de calcul sur plusieurs centaines d’itérations.

Critère raisonnable attendu (non strict) :
un agent doit répondre en moins d’1 ms par action.
C’est seulement une référence, pas une contrainte obligatoire.

4.2 Consommation mémoire

Test prévu :

Faire jouer l’agent sur plusieurs milliers de coups

Vérifier qu’il ne crée pas d’objets inutiles au fil du temps

On veut éviter des fuites mémoire ou des structures qui grandissent sans raison.

4.3 Scalabilité

J’évalue l’agent sur différents formats :

petits masques (9 actions)

moyens (81 actions)

grands (361 actions)

Puis je rejoue plusieurs milliers de coups pour voir si la performance reste stable.

5. Tests stratégiques

Ces tests ne portent pas sur la validité, mais sur la qualité du jeu.

5.1 Victoires contre un agent aléatoire

Je fais jouer SmartAgent contre RandomAgent sur 100+ parties.

Résultats attendus :

SmartAgent doit gagner la majorité (au moins > 60 %)

Quelques égalités sont normales

RandomAgent ne doit pas gagner souvent

Dans mes premiers tests, j’ai obtenu :
67 victoires – 0 défaites – 33 nuls,
ce qui est cohérent avec l’idée d’un agent plus rationnel qu’un agent totalement aléatoire.

5.2 Capacité à bloquer et saisir les opportunités

Tests artificiels :

Position où l’adversaire peut gagner en un coup → SmartAgent doit bloquer.

Position où SmartAgent peut gagner immédiatement → il doit saisir l’occasion.

Cela permet d’évaluer si l’agent comprend au moins les “obvious moves”.

5.3 Stabilité du comportement

Objectifs :

Vérifier que l’agent ne renvoie pas des décisions incohérentes

Tester s’il joue systématiquement le même coup en situation déterministe (si applicable)

Vérifier qu’il varie correctement si de l’aléatoire est introduit

6. Tests de robustesse

Ces tests simulent des conditions extrêmes.

Idées :

Générer 1 000 masques complètement aléatoires et les envoyer aux agents

Jouer 10 000 coups d’affilée pour détecter d’éventuels crashs

Tester l’agent avec des entrées volontairement cassées (fuzzing)

Le but est d’assurer que l’agent ne plante pas dans une situation imprévue.

7. Tests d’intégration

Ces tests vérifient que les agents fonctionnent correctement dans un vrai environnement de jeu.

Comprend :

Simulations complètes avec un moteur de jeu

Tests reproductibles avec une seed

Comparaison systématique SmartAgent vs RandomAgent vs baseline

8. Conclusion

La stratégie de test couvre :

la validité des décisions des agents (tests fonctionnels)

leur fiabilité dans le temps (performance et robustesse)

leur intelligence minimale (tests stratégiques)

leur comportement dans un cadre réel (intégration)

L’ensemble de ces tests permet de garantir que les agents se comportent correctement, qu’ils ne violent pas les règles du jeu, et qu’ils restent stables et performants lorsqu’ils sont utilisés dans des simulations complètes.



1.2 Comment tester ?

Pour chaque catégorie, voici l’approche que j’utiliserai.

A. Tests fonctionnels

Coups valides

Construire des action_mask spécifiques

Vérifier que l’action choisie ∈ valid_actions

Position de fin de partie

Fournir un plateau final et vérifier que l’agent ne crash pas.

Détection d’un coup gagnant

Construire un plateau où placer dans la colonne X donne la victoire

Vérifier que _find_winning_move renvoie X

Double menace

Simuler un plateau où un coup crée deux alignements potentiels

Vérifier que _creates_double_threat → True

Tests réalisés via pytest.

B. Tests de performance

Temps moyen par coup

Utiliser time.time() autour de choose_action()

Répéter sur 500 appels

Mémoire utilisée

import tracemalloc

Surveiller l’évolution de la mémoire sur plusieurs centaines d’appels

Stress test

Exécuter 1000 parties RandomAgent vs SmartAgent

S’assurer que SmartAgent reste stable

C. Tests stratégiques

Taux de victoire

Script qui joue 100 parties automatiques

Stocker les statistiques (victoire, défaite, nul)

Tournoi multi-agents

SmartAgent vs RandomAgent

SmartAgent vs SmartAgent

RandomAgent vs RandomAgent (baseline)

Analyse qualitative

Sur quelques parties, vérifier manuellement les logs (loguru) :

coup gagnant détecté

coup de blocage utilisé

sélection du centre

1.3 Critères de succès

Voici les critères que je considère comme satisfaisants pour valider la qualité de mon agent intelligent.

Fonctionnels

L’agent ne doit jamais jouer un coup invalide.

Les fonctions internes doivent donner des résultats cohérents :

_find_winning_move détecte 100 % des cas simples

_get_valid_actions renvoie toujours une liste correcte

Performance

Temps moyen par coup < 0.05 secondes
(cela laisse une grande marge ; en pratique l’agent est beaucoup plus rapide)

Mémoire utilisée stable, pas de fuite après 1000 appels.

Stratégiques

SmartAgent gagne au moins 60 % des parties contre RandomAgent,
idéalement > 70 %.

SmartAgent ne doit jamais manquer un coup gagnant accessible.

SmartAgent doit bloquer plus de 95 % des menaces évidentes.

Ces critères me semblent raisonnables pour un agent basé sur des règles simples, sans recherche de profondeur ni minimax.
