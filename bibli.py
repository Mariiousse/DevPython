import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class GestionLivresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Livres")
        self.root.geometry("550x450")
        tabControl = ttk.Notebook(self.root)

        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect('bibliotheque.db')
        self.cursor = self.conn.cursor()

        # Création de la table Livres si elle n'existe pas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT,
                auteur TEXT,
                genre TEXT,
                isbn TEXT
            )
        ''')
        self.conn.commit()
        # Interface utilisateur
        # self.frame = tk.Frame(tabControl)
        # self.frame.pack(padx=10, pady=10)
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
  
        tabControl.add(tab1, text ='Gestion livres')
        tabControl.add(tab2, text ='Gestion utilisateurs')
        tabControl.pack(expand = 1, fill ="both")
        
       
        tk.Label(tab1, text="Titre:").grid(row=0, column=0, )
        tk.Label(tab1, text="Auteur:").grid(row=1, column=0, )
        tk.Label(tab1, text="Genre:").grid(row=2, column=0, )
        tk.Label(tab1, text="ISBN:").grid(row=3, column=0, )

        self.titre_entry = tk.Entry(tab1)
        self.auteur_entry = tk.Entry(tab1)
        self.genre_entry = tk.Entry(tab1)
        self.isbn_entry = tk.Entry(tab1)

        self.titre_entry.grid(row=0, column=1)
        self.auteur_entry.grid(row=1, column=1)
        self.genre_entry.grid(row=2, column=1)
        self.isbn_entry.grid(row=3, column=1)

        # Boutons
        tk.Button(tab1, text="Ajouter Livre", command=self.ajouter_livre).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(tab1, text="Rechercher Livre", command=self.rechercher_livre).grid(row=5, column=0, columnspan=2, pady=10)
        
    def ajouter_livre(self):
        titre = self.titre_entry.get()
        auteur = self.auteur_entry.get()
        genre = self.genre_entry.get()
        isbn = self.isbn_entry.get()

        if titre and auteur and genre and isbn:
            # Ajouter le livre à la base de données
            self.cursor.execute('''
                INSERT INTO Livres (titre, auteur, genre, isbn)
                VALUES (?, ?, ?, ?)
            ''', (titre, auteur, genre, isbn))
            self.conn.commit()

            messagebox.showinfo("Succès", "Livre ajouté avec succès.")
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    def rechercher_livre(self):
        titre = self.titre_entry.get()

        if titre:
            # Rechercher le livre par titre
            self.cursor.execute('''
                SELECT * FROM Livres WHERE titre LIKE ?
            ''', ('%' + titre + '%',))
            livres = self.cursor.fetchall()

            if livres:
                result_str = "Résultats de la recherche :\n"
                for livre in livres:
                    result_str += f"{livre[1]} par {livre[2]}, ISBN: {livre[4]}\n"

                messagebox.showinfo("Résultats", result_str)
            else:
                messagebox.showinfo("Résultats", "Aucun livre trouvé.")
        else:
            messagebox.showerror("Erreur", "Veuillez saisir un titre pour la recherche.")

    

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionLivresApp(root)
    root.mainloop()