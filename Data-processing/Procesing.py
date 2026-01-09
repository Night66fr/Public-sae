from utils import *

def convertir_en_variables(dictionnaire):
    for cle, valeurs in dictionnaire.items():
        nom_variable = cle.replace(" ", "_").replace("-", "_")
        print(f"{nom_variable} = {valeurs}")

print(convertir_en_variables(a))