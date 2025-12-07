1. Il faut vérifier les victoires avant les blocages car gagner termine immédiatement la partie, alors que bloquer n’est utile que si je ne peux pas gagner moi-même.

2. Victoire horizontale : on compte les pions alignés à gauche et à droite.
   Victoire verticale : on compte les pions alignés au-dessus et au-dessous.

3. On simule le placement d’un pion car l’état actuel du board ne contient pas encore le coup hypothétique. On doit tester l’état futur.

4. La complexité de la détection de victoire est O(1) par coup testé, et O(7) pour tester toutes les colonnes.

5. Cas limites :
   - colonnes pleines
   - diagonales partiellement hors du plateau
   - coups situés en bordure
   - action_mask qui désactive certaines colonnes

