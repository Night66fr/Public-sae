from math import * 

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