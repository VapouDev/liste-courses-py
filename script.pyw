import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

# Fonction pour lire le fichier des recettes et les charger dans un dictionnaire
def lire_recettes(fichier):
    recettes = {}
    with open(fichier, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    plat = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not line.startswith('-'):
            plat = line
            recettes[plat] = {}
        else:
            try:
                ingredient, quantite = line.split(': ')
                recettes[plat][ingredient] = quantite
            except ValueError:
                print(f"Erreur de format dans la ligne : {line}")
    return recettes

# Fonction pour générer la liste de courses
def generer_liste_courses(selection):
    courses = defaultdict(int)
    for plat in selection:
        for ingredient, quantite in recettes[plat].items():
            try:
                quantite_valeur, quantite_unite = quantite.split()
                courses[ingredient] += int(quantite_valeur)
            except ValueError:
                print(f"Erreur de format pour l'ingrédient {ingredient} avec la quantité {quantite}")
    return courses

# Fonction pour afficher la liste de courses
def afficher_liste_courses():
    selection = [var.get() for var in check_vars if var.get()]
    if not selection:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins un plat.")
        return
    liste_courses = generer_liste_courses(selection)
    fenetre_courses = tk.Toplevel(root)
    fenetre_courses.title("Liste de Courses")
    fenetre_courses.configure(bg='#333333')
    text = tk.Text(fenetre_courses, bg='#333333', fg='#ffffff', font=('Arial', 14))
    for ingredient, quantite in liste_courses.items():
        text.insert(tk.END, f"{ingredient}: {quantite}\n")
    text.pack(padx=20, pady=20)

# Configuration de la fenêtre principale
root = tk.Tk()
root.title("Liste de Courses")
root.configure(bg='#333333')
root.geometry('600x400')

# Lecture des recettes depuis le fichier
recettes = lire_recettes('recettes.txt')

# Label principal
label_titre = tk.Label(root, text="Sélectionnez les plats pour générer votre liste de courses", bg='#333333', fg='#ffffff', font=('Arial', 16))
label_titre.pack(pady=20)

# Affichage des plats dans une liste avec des checkbuttons
check_vars = []
frame_list = tk.Frame(root, bg='#333333')
frame_list.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
for plat in recettes.keys():
    var = tk.StringVar(value=plat)
    check_vars.append(var)
    cb = tk.Checkbutton(frame_list, text=plat, variable=var, onvalue=plat, offvalue="", bg='#333333', fg='#ffffff', selectcolor='#0000ff', font=('Arial', 14))
    cb.pack(anchor='w')

# Bouton pour générer la liste de courses
bouton_generer = tk.Button(root, text="Générer la Liste de Courses", command=afficher_liste_courses, bg='#555555', fg='#ffffff', font=('Arial', 14), activebackground='#666666', activeforeground='#ffffff')
bouton_generer.pack(pady=20)

# Lancement de l'application
root.mainloop()
