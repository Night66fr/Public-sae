import json
import matplotlib.pyplot as plt
from datetime import datetime

def tracer_occupation_parking(nom_fichier, nom_parking):
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {nom_fichier} est introuvable.")
        return

    temps_list = []
    occupation_list = []
    
    # On s'assure que 'donnees' est bien une liste
    if not isinstance(donnees, list):
        print("Erreur : Le format du JSON n'est pas une liste d'objets.")
        return

    for entree in donnees:
        # .get('id') renvoie None au lieu de faire une erreur si la clé manque
        if isinstance(entree, dict) and entree.get('id') == nom_parking:
            try:
                # Conversion du temps
                dt = datetime.strptime(entree['temps'], "%d/%m/%Y %H:%M:%S")
                
                # Conversion de l'occupation (on enlève le % et on convertit en float)
                occ_val = float(entree['place']['occupation'].replace('%', ''))
                
                temps_list.append(dt)
                occupation_list.append(occ_val)
            except (KeyError, ValueError) as e:
                # On ignore les entrées où 'temps' ou 'place' manqueraient
                continue
    
    if not temps_list:
        print(f"Aucune donnée trouvée pour le parking : {nom_parking}")
        return

    # Tri par date pour éviter les lignes emmêlées
    donnees_triees = sorted(zip(temps_list, occupation_list))
    temps_list, occupation_list = zip(*donnees_triees)

    # Création du graphique
    plt.figure(figsize=(10, 5))
    plt.plot(temps_list, occupation_list, marker='o', color='red', markersize=4)
    plt.title(f"Occupation du parking {nom_parking} au cours du temps")
    plt.xlabel("Date et Heure")
    plt.ylabel("Occupation (%)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
# Utilisation de la fonction avec votre fichier
parking_demander = input("parking que tu veux voir en graphe : ")

tracer_occupation_parking('Donnée_SAE_Parking', 'Montpellier')
