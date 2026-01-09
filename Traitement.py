import json

def extraire_tendances_occupation(nom_fichier_source):
    # 1. Charger les données brutes
    try:
        with open(nom_fichier_source, "r", encoding="utf8") as f:
            donnees_brutes = json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {nom_fichier_source} est introuvable.")
        return
    except json.JSONDecodeError:
        print("Erreur : Le fichier JSON est mal formé.")
        return

    # 2. Dictionnaire pour stocker les listes d'occupation
    # Structure : { "Nom du Parking": [valeur1, valeur2, ...] }
    resultat_final = {}

    for entree in donnees_brutes:
        # On détermine le nom (soit 'id' pour un parking, soit 'type' pour le global Montpellier)
        nom_parking = entree.get("id") or entree.get("type")
        
        if nom_parking and "place" in entree:
            # Récupérer la chaîne "34.23%" et la transformer en nombre (float) 34.23
            occupation_str = entree["place"]["occupation"]
            occupation_valeur = float(occupation_str.replace('%', ''))

            # Si le parking n'est pas encore dans le dictionnaire, on crée une liste vide
            if nom_parking not in resultat_final:
                resultat_final[nom_parking] = []
            
            # On ajoute la valeur à la liste du parking correspondant
            resultat_final[nom_parking].append(occupation_valeur)

    return resultat_final

# --- Exécution ---
nom_fichier = "Donnée_SAE_Parking"
stats_occupations = extraire_tendances_occupation(nom_fichier)

if stats_occupations:
    # Affichage du résultat pour vérifier (Ex: Polygone)
    if "Polygone" in stats_occupations:
        print(f"Données pour Polygone : {stats_occupations['Polygone']}")

    # 3. Sauvegarder ce nouveau format dans un fichier JSON séparé
    with open("Occupation_Par_Parking.json", "w", encoding="utf8") as f_out:
        json.dump(stats_occupations, f_out, indent=4, ensure_ascii=False)
    
    print("\nLe fichier 'Occupation_Par_Parking.json' a été généré avec succès.")

import json

def extraire_tendances_velo(nom_fichier_source):
    # 1. Charger les données brutes des vélos
    try:
        with open(nom_fichier_source, "r", encoding="utf8") as f:
            donnees_brutes = json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {nom_fichier_source} est introuvable.")
        return
    except json.JSONDecodeError:
        print("Erreur : Le fichier JSON est mal formé.")
        return

    # 2. Dictionnaire pour stocker les listes d'occupation par station
    resultat_final = {}

    for entree in donnees_brutes:
        # On récupère l'identifiant de la station (id)
        nom_station = entree.get("id")
        
        if nom_station and "place" in entree:
            # Récupérer "75.0%" et le transformer en 75.0
            try:
                occupation_str = entree["place"]["occupation"]
                occupation_valeur = float(occupation_str.replace('%', ''))

                # Initialiser la liste si la station apparaît pour la première fois
                if nom_station not in resultat_final:
                    resultat_final[nom_station] = []
                
                # Ajouter la valeur à l'historique de la station
                resultat_final[nom_station].append(occupation_valeur)
            except (ValueError, KeyError):
                # En cas de donnée mal formée, on passe à la suivante
                continue

    return resultat_final

# --- Exécution ---
nom_fichier_entree = "Donnée_SAE_velo"
stats_velo = extraire_tendances_velo(nom_fichier_entree)

if stats_velo:
    # Exemple d'affichage pour une station (ex: Gare Saint-Roch)
    # On affiche les premières stations trouvées pour vérifier
    premieres_stations = list(stats_velo.keys())[:3]
    print("Aperçu des données extraites :")
    for s in premieres_stations:
        print(f"{s} : {stats_velo[s]}")

    # 3. Sauvegarder dans un nouveau fichier JSON
    nom_fichier_sortie = "Occupation_Par_Station_Velo.json"
    with open(nom_fichier_sortie, "w", encoding="utf8") as f_out:
        json.dump(stats_velo, f_out, indent=4, ensure_ascii=False)
    
    print(f"\nFichier '{nom_fichier_sortie}' créé avec succès.")