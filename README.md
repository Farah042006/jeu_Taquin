🧩 Jeu du Taquin 3x3 avec Algorithme A*
Ce projet associe une interface graphique interactive (tkinter) à un moteur de résolution intelligent basé sur l'algorithme de recherche A*.

✨ Fonctionnalités principales
Interface Graphique Intuitive (tkinter) :
Affichage visuel du damier 3x3 en temps réel.
Saisie personnalisée et validation de l'état final par l'utilisateur (chiffres de 0 à 8).
Journal de bord interactif avec barre de défilement pour suivre pas à pas les étapes de l'exploration de l'algorithme.

Moteur d'IA (Algorithme A*) :
Utilisation de l'heuristique de la distance de Manhattan (ou des tuiles mal placées).
Vérification préalable de la solubilité de la grille grâce au calcul de la parité des inversions.

Animation de la solution :
Visualisation fluide de la séquence optimale de mouvements pour résoudre le taquin de l'état initial jusqu'à l'état final.

🗂️ Structure du projet
Le projet est divisé en deux modules principaux :
interface.py : Gère toute la partie graphique, les interactions utilisateur, l'affichage du plateau sur un Canvas, et le déclenchement des animations.
puzzle.py : Contient la logique mathématique du jeu, la gestion des voisins, le calcul de l'heuristique, le test de solubilité et l'algorithme A*.

## 📺 Démonstration vidéo
Regardez une démonstration de l'exécution du programme ici :
👉 [Lien vers la vidéo de démonstration](https://youtu.be/hjY_DBGRSmY)
