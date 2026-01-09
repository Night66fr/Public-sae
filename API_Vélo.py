import requests
import time
import json
import os

def convertir_temps(temps_unix):
    structure_temps = time.localtime(temps_unix)
    date_lisible = time.strftime("%d/%m/%Y %H:%M:%S", structure_temps)
    return date_lisible

nom_fichier = "Donnée_SAE_velo"

temps_arret_heure = 1
temps_arret_minutes = temps_arret_heure*60
temps_arret_seconde = temps_arret_minutes*60 

duree_jour = 30
duree_heure = duree_jour*24 
duree_minutes = duree_heure*60
duree_secondes = duree_minutes*60

nb_mesures = duree_secondes//temps_arret_seconde

for i in range(nb_mesures):
    temps_actuel = convertir_temps(time.time())
    reponse_velo = requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
    data_velo = reponse_velo.json()     
    resultat = []
    velo_total_ville = 0
    velo_occuper_ville = 0
    velo_libre_ville = 0 
    for velo in data_velo:
        if velo['status']['value'] == 'working':
            velo_total = velo["totalSlotNumber"]["value"]
            velo_disponible = velo["availableBikeNumber"]["value"]
            velo_occuper = velo['freeSlotNumber']['value']
            pourcentage = (velo_occuper/velo_total)*100
            resultat.append({ 
                "id": velo["address"]["value"]["streetAddress"],
                "status": velo['status']['value'],
                "temps": temps_actuel,
                "place": { 
                    "velo_total" : velo_total,
                    "velos_occupee": velo_occuper,
                    "velos_disponibles": velo_disponible,
                    "occupation": f"{round(pourcentage,2)}%"
                    }
                }) 

            velo_total_ville += velo_total
            velo_occuper_ville += velo_occuper
            velo_libre_ville += velo_disponible
    pourcent_global = round((velo_occuper_ville / velo_total_ville) * 100, 2)
    resultat.append({
        "type": "Montpellier",
        "temps": temps_actuel,
        "place": {
            "velo_total": velo_total_ville,
            "velos_occupee": velo_occuper_ville,
            "velos_disponibles": velo_libre_ville,
            "occupation": f"{pourcent_global}%"
            }
        })

    if os.path.exists(nom_fichier): #demander à l'IA pour pouvoir enregistrer et que je puisse le voir directement 
        with open(nom_fichier, "r", encoding="utf8") as f:
            try:
                    contenu = json.load(f)
            except:
                    contenu = []
    else:
        contenu = []
        
    contenu.extend(resultat)
    with open(nom_fichier, "w", encoding="utf8") as f:
        json.dump(contenu, f, indent=4, ensure_ascii=False)

    print(f"Mesure vélo {i+1} enregistrée à {temps_actuel}")
   
    if i < nb_mesures - 1:
        time.sleep(temps_arret_seconde-1)      