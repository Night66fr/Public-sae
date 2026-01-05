from math import * 

data1 = [3,3,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,8,7,4]
data2 = [103,203,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,-92,-93,-96]

data_liste = [[3,3,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,8,7,4],
              [103,203,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,-92,-93,-96],
              [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]

def Moyenne(data): 
    resultat = 0 
    a = len(data)
    for i in range(0,a): 
        resultat += data[i]
    resultat = resultat/a
    return resultat


def Variance(data): 
    resultat = 0
    Ex = Moyenne(data) 
    a = len(data)
    for i in range(0,a): 
        resultat += (data[i]-Ex)**2
    resultat = resultat/a 
    return resultat

def Ecart_type(data):
    resultat = sqrt(Variance(data))
    return resultat

def Corvariance(data1,data2) : 
    resultat = 0 
    Ex = Moyenne(data1)
    Ey = Moyenne(data2)
    a = len(data1)
    b = len(data2)
    if a >= b :
        valeur = b
    elif b >= a :
        valeur = a 
    for i in range(0,valeur): 
        resultat += (data1[i]-Ex)*(data2[i]-Ey)
    resultat = resultat/valeur
    return resultat

def Corelation(data1,data2):
    resultat = 0
    cov = Corvariance(data1,data2)
    racine_sigma_x_y = sqrt(Ecart_type(data1)*Ecart_type(data2))
    resultat = cov/racine_sigma_x_y
    return resultat

def Corelation_bornée(data1,data2):
    resultat = 0
    cov = Corvariance(data1,data2)
    racine_sigma_x_y = (Ecart_type(data1)*Ecart_type(data2))
    resultat = cov/racine_sigma_x_y
    return resultat     

def matrice(data_liste) : 
    resultat = []
    a = len(data_liste)
    for i in range(0,a):
        temporaire = []
        for j in range(0,a) :
            temporaire.append(Corvariance(data_liste[i],data_liste[j]))
        resultat.append(temporaire)
    return resultat

"""
print(f"La moyenne est de {Moyenne(data1)}")
print(f"L'écart-type est de {Ecart_type(data1)}")
print(f"La Covariance est de {Corvariance(data1,data2)}")
print(f"La Corelation est de {Corelation(data1,data2)}")
"""
print(matrice(data_liste))