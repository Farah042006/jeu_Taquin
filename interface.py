import tkinter as tk
from logging import root
from struct import pack

from puzzle import initial_state, A_star, est_solvable

"""la couleur de fond"""
FOND = "#f0f0f0"
CAP1 = "1. L'état initial"
CAP2 = "2.Saisit l'état final (0 = case vide)"
CAP3 = "3. 9 chiffres différents"
CAP4 = "4. Clic sur résoudre"
CAP5 = "5. Animation de la solution"

"""écrit un damier sur une ligne"""
def en_texte(etat):
    lignes = []
    for l in range(3):
        lignes.append(" ".join("_" if v == 0 else str(v) for v in etat[l * 3:l * 3+ 3]))
    return " / ".join(lignes)

class App:
    def __init__(self, root):
        self.root = root
        root.title("Jeux TAQUIN - Algorithme A*")
        root.geometry("960x560")
        root.resizable(False, False)
        root.configure(bg = FOND)
        self.etat = initial_state
        self.final = None
        self.occupe = False

        # partie gauche
        gauche = tk.Frame(root, bg=FOND, width=370, height=520)
        gauche.grid(row=0, column=0, sticky="n")
        gauche.pack_propagate(False)

        tk.Label(gauche, text="État initial ", font=("Arial", 12, "bold"), bg=FOND).pack(pady=(20, 5))

        self.Canvas = tk.Canvas(gauche, width=220, height=220, bg=FOND, highlightthickness=0)
        self.Canvas.pack()
        tk.Label(gauche, text="État final(9 chiffres, 0 = vide) : ", bg=FOND).pack(pady=(15, 3))
        self.entree = tk.Entry(gauche, width=12, font=("Arial", 16))
        self.entree.pack(pady=3)
        self.entree.bind("<KeyRelease>", lambda e: self.legende(CAP2))
        tk.Button(gauche, text="Valider l'état final", width=20, command=self.valider).pack(pady=5)
        self.info = tk.Label(gauche, text="", fg="#1a3fd0", bg=FOND, wraplength=330)
        self.info.pack()
        self.erreur = tk.Label(gauche, text="", fg="red", bg=FOND, wraplength=330)
        self.erreur.pack()

        bouton = tk.Frame(gauche, bg=FOND)
        bouton.pack(pady=10)
        tk.Button(bouton, text="Résoudre ( A*)", width=14, command=self.resoudre).pack(side="left", padx=5)

        # partie droite
        droite = tk.Frame(root, bg=FOND)
        droite.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        self.log = tk.Text(droite, width=66, height=27, font=("Courier", 11), bg="white", relief="solid", borderwidth=1)
        self.log.pack(side="left")
        sb = tk.Scrollbar(droite, command=self.log.yview)
        sb.pack(side="left", fill="y")
        self.log.config(yscrollcommand=sb.set)

        self.text_legende = tk.StringVar(value=CAP1)
        tk.Label(root, textvariable=self.text_legende, bg="#1f2937", fg="white",
                 font=("Arial", 13, "bold"), anchor="w", padx=20, pady=8).grid(row=1, column=0, columnspan=2, sticky="ew")

        self.afficher()

    def legende(self, texte):
        self.text_legende.set(texte)

    def afficher(self):
        self.Canvas.delete("all")
        taille = 72
        for i, v in enumerate(self.etat):
            x = 4 + (i % 3) * taille  # colonne
            y = 4 + (i // 3) * taille  # ligne
            self.Canvas.create_rectangle(x, y, x+taille, y+taille, fill="white", outline="#222", width=2)
            if v != 0:
                self.Canvas.create_text(x + taille / 2, y + taille / 2, text=str(v), font=("Arial", 28))

    def valider(self):
        if self.occupe:  # ignoré pendant l’animation
            return
        texte = self.entree.get().replace(" ", "").replace(",", "")
        if len(texte) != 9 or not texte.isdigit():
            self.erreur.config(text="Tape exactement 9 chiffres, par exemple 123456780")
            return
        etat = tuple(int(c) for c in texte)  # conversion en tuple
        if sorted(etat) != list(range(9)):
            self.erreur.config(text="Utilise chaque chiffre de 0 à 8 une seule fois.")
            return
        if not est_solvable(etat, initial_state):
            self.erreur.config(text="Cette configuration est impossible à atteindre. Essaie-en une autre.")
            return
        self.erreur.config(text="")  # efface un éventuel ancien message rouge
        self.final = etat
        self.info.config(text="État final : " + en_texte(etat))
        self.legende(CAP3)

    def reinitialiser(self):
        if self.occupe:
            return
        self.etat = initial_state
        self.final = None
        self.entree.delete(0, "end")  # vide le champ de saisie
        self.info.config(text="")  # efface le messages
        self.erreur.config(text="")
        self.log.delete("1.0", "end")
        self.legende(CAP1)
        self.afficher()  # redessine le damier

    def resoudre(self):
        if self.occupe:
            return
        if self.final is None:
            self.erreur.config(text="Valide d'abord un état final.")
            return

        self.erreur.config(text="")
        self.occupe = True  # verrouille les boutons
        self.etat = initial_state
        self.afficher()
        self.log.delete("1.0", "end")
        chemin, etapes = A_star(initial_state, self.final)  # lance la recherche
        self.legende(CAP4)
        self.montrer_exploration(chemin, etapes, 0)

    def montrer_exploration(self, chemin, etapes, k):  # k est le numéro de l’exploration à afficher
        if k < len(etapes):
            etat, g, h, f = etapes[k]
            self.log.insert("end", f"Exploration {k + 1} : g={g} h={h} f={f}\n")
            for r in range(3):
                ligne = " ".join(" " if v == 0 else str(v) for v in etat[r * 3:r * 3 + 3])
                self.log.insert("end", f"  {ligne}\n")
            self.log.insert("end", "\n")
            self.log.see("end")  # fait défiler vers le bas.
            self.root.after(1600, lambda: self.montrer_exploration(chemin, etapes, k + 1))
        else:
            self.log.insert("end", f"Solution en {len(chemin) - 1} déplacements.\n")
            self.log.see("end")
            self.legende(CAP5)
            self.root.after(1200, lambda: self.animer(chemin, 0))

    def animer(self, chemin, k):
        if k < len(chemin):
            self.etat = chemin[k]
            self.afficher()
            self.root.after(1000, lambda: self.animer(chemin, k + 1))
        else:
            self.legende(f"Résultat : solution optimale en {len(chemin) - 1} déplacements")
            self.occupe = False

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()  # garde la fenêtre ouverte















