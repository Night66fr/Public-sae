from utils import *

data1 = [3,3,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,8,7,4]
data2 = [103,203,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,-92,-93,-96]

data_liste = [[3,3,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,8,7,4],
              [103,203,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,-92,-93,-96],
              [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]

print(f"La moyenne est de {Moyenne(data1)}")
print(f"L'écart-type est de {Ecart_type(data1)}")
print(f"La Covariance est de {Corvariance(data1,data2)}")
print(f"La Corelation est de {Corelation(data1,data2)}")
print(matrice(data_liste))