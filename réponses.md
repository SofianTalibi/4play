# Questions d’auto-vérification – SmartAgent

Voici mes réponses aux questions d’auto-vérification de l’exercice 3 sur l’agent basé sur des règles.

---

## 1. Pourquoi vérifier les victoires avant les blocages ?
Il faut vérifier si je peux gagner avant de bloquer l’adversaire parce qu’un coup gagnant termine la partie directement. Bloquer ne sert que si je ne peux pas gagner moi-même ce tour-là.

---

## 2. Comment détecter une victoire verticale vs une victoire horizontale ?
- Horizontale : je compte les pions alignés à gauche et à droite du coup que je viens de jouer.  
- Verticale : je compte les pions alignés au-dessus et en dessous du coup.

---

## 3. Pourquoi simuler le placement d’un pion avant de vérifier les victoires ?
Parce que le plateau actuel ne contient pas encore ce coup. Il faut simuler pour voir si, après avoir joué, ça crée une victoire.

---

## 4. Complexité de l’algorithme de détection de victoire
- Vérifier un coup : O(1), le plateau a une taille fixe.  
- Vérifier toutes les colonnes possibles : O(7), donc toujours constant.

---

## 5. Cas limites à prendre en compte
- Colonnes pleines  
- Diagonales qui dépassent du plateau  
- Coups sur les bords  
- Colonnes désactivées par `action_mask`


