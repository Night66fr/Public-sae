import requests
import time
import json
import os

def convertir_temps(temps_unix):
    structure_temps = time.localtime(temps_unix)
    date_lisible = time.strftime("%d/%m/%Y %H:%M:%S", structure_temps)
    return date_lisible

nom_fichier = "Donnée_SAE_Parking"

temps_arret_heure = 1
temps_arret_minutes = temps_arret_heure*60
temps_arret_seconde = temps_arret_minutes*60

duree_jour = 30
duree_heure = duree_jour*24 
duree_minutes = duree_heure*60
duree_secondes = duree_minutes*60

nb_mesures = duree_secondes//temps_arret_seconde

for i in range(int(nb_mesures)):
    temps_actuel = convertir_temps(time.time())
    reponse_parking = requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    data_parking = reponse_parking.json()       
    resultat = []
    emplacement_ville_total = 0 
    emplacement_ville_occuper = 0 
    emplacement_ville_libre = 0
    for place in data_parking:
        if place['status']['value'] == 'Open':
            emplacement_total = place["totalSpotNumber"]["value"]
            emplacement_libres = place['availableSpotNumber']['value']
            emplacement_occupe = emplacement_total - emplacement_libres
            pourcent = round((emplacement_occupe/emplacement_total)*100,2) 
            resultat.append({
                "id": place["name"]['value'],
                "status": place['status']['value'],
                "temps": temps_actuel,
                "place": {
                    "emplacement_total": emplacement_total,
                    "emplacement_occupe" : emplacement_occupe, 
                    "emplacement_disponible": emplacement_libres,
                    "occupation": f"{pourcent}%"
                }
            })
            emplacement_ville_total += emplacement_total
            emplacement_ville_occuper += emplacement_occupe
            emplacement_ville_libre += emplacement_libres
    pourcent_global = round((emplacement_ville_occuper / emplacement_ville_total) * 100, 2)
    resultat.append({
        "type": "Montpellier",
        "temps": temps_actuel,
        "place": {
            "emplacement_total": emplacement_ville_total,
            "emplacement_occupe": emplacement_ville_occuper,
            "emplacement_disponible": emplacement_ville_libre,
            "occupation": f"{pourcent_global}%"
            }
        })
        
    if os.path.exists(nom_fichier): #demander à l'IA pour pouvoir enregistrer et que je puisse le voir directement 
        with open(nom_fichier, "r", encoding="utf8") as f:
            try:
                contenu = json.load(f)
            except json.JSONDecodeError:
                contenu = []
    else:
        contenu = []

    contenu.extend(resultat) 
    with open(nom_fichier, "w", encoding="utf8") as f:
        json.dump(contenu, f, indent=4, ensure_ascii=False)

    print(f"Mesure parking {i+1} enregistrée {temps_actuel}")

    if i < nb_mesures - 1:
        time.sleep(temps_arret_seconde-1)  