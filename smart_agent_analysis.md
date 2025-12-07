# Analyse de performance de SmartAgent

## Résultats du tournoi contre RandomAgent

- Nombre de parties jouées : 100
- SmartAgent a gagné : 100
- RandomAgent a gagné : 0
- Matchs nuls : 0

## Efficacité de la stratégie

- Règle déclenchée le plus souvent :
  1. Centre préféré (coup central)
  2. Blocage de l’adversaire
  3. Coup gagnant immédiat
- La règle du double menace n’est pas encore implémentée.

## Cas d’échec

- Les matchs nuls surviennent généralement lorsque :
  - Les deux agents remplissent alternativement le centre et les bords.
  - Aucun coup gagnant immédiat n’est disponible.

## Améliorations possibles

- Implémenter la détection des doubles menaces pour rendre l’agent imbattable.  
- Ajouter une pondération stratégique pour préférer les colonnes centrales et éviter les positions vulnérables.  
- Optimiser la simulation pour anticiper deux tours à l’avance.

## Conclusion

SmartAgent bat systématiquement un agent aléatoire sur 100 parties et démontre la supériorité des heuristiques de base (victoire immédiate, blocage, centre). Les améliorations stratégiques peuvent encore renforcer sa robustesse.

