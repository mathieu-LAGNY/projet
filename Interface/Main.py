#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:39:15 2020

@author: mathieu
"""
#import time
from copy import deepcopy

"-------------------------------------------------------------"

"""Récupération des informations du document table"""


#.............................................................................
#E         chaine, variable de type '35.967545106(29)'
#Action    Permet d'enlever les parenthèses contenant l'incertitude
#S         La valeur de la chaine en float 35.967545106
def enlever_incertitudes(chaine):
    i = 0
    for caractere in chaine:
        if caractere == "(":
            return float(chaine[:i])
        else:
            i += 1
    return float(chaine)
#.............................................................................

#.............................................................................
#E         v, variable quelconque de type quelconque.
#Action    Permet de vérifier si une variable est un entier.
#S         True si v est un entier, False sinon.
def is_number(v):
    try :
        var = int(v)
        return True
    except :
        return False
#.............................................................................

#.............................................................................
#E         filename,  le nom du fichier contenant les abondances.
#Action    Permet de récupérer les valeurs des abondances isotopiques depuis un fichier texte
#S         abondances,  un dictionnaire dont les indices sont les symboles chimiques des atomes
def upload_abondances(filename="./../abondances/abondances.txt"):
    table = open(filename,"r")
    tableau = table.read().split("\n")
    abondances = {}

    # On enlève d'abord tous les espaces
    for i in range(len(tableau)):
        ligne = tableau[i].split(" ")
        nouvelle_ligne = []
        for case in ligne:
            if case != '':
                nouvelle_ligne.append(case)
        tableau[i] = nouvelle_ligne
    
    # Puis remplit  le dictionnaire avec les couples masse  abondance
    symbole = ""
    tableau_couples = []
    for i in range(len(tableau)):
        ligne = tableau[i]
        if len(ligne) == 4:  # Il s'agit d'un nouvel élément
            if i != 0: # Si on n'est pas sur la première ligne
                abondances[symbole] = tableau_couples # On ajoute le tableau de l'élément précédent
                tableau_couples = []
            for j in range(len(ligne[1])): # On récupère le symbole
                if not is_number(ligne[1][j]):
                    symbole = ligne[1][j:]
                    break

            masse = enlever_incertitudes(ligne[2])
            abondance = enlever_incertitudes(ligne[3])
            tableau_couples.append([masse,abondance]) # On ajoute la ligne dans le tableau
        elif  len(ligne) == 2: # Il s'agit d'un élément inexistant naturellement
            abondances[ligne[1]] = []          
        else: # Il s'agit d'une nouvelle ligne de l'élément actuel
            masse = enlever_incertitudes(ligne[1])
            abondance = enlever_incertitudes(ligne[2])
            tableau_couples.append([masse,abondance]) # On ajoute la ligne dans le tableau
    
    # On utilise le produit en croix pour avoir les abondances dans le bon format pour le calcul
    for atome in abondances.keys():
        tableau_couples = abondances[atome]
        abondance_max = 0.
        for couple in tableau_couples:
            if couple[1] > abondance_max:
                abondance_max = couple[1]
        for couple in tableau_couples:
            couple[1] = 100*couple[1]/abondance_max
            
    table.close()
    return abondances
#.............................................................................

"-------------------------------------------------------------"

"""Fonctions de lecture d'une formule brute"""
       
#.............................................................................
#E         fb, la formule brute à traiter, abondances, un dictionnaire contenant les abondances
#Action    Permet d'analyser la formule brute et de connaître les atomes utilisés ainsi que leurs nombres.
#S         tableau de couples ["Symbole chimique", nombre d'atomes]
def lecture_FB(fb,abondances=upload_abondances()):  
    if (fb != ""):
        tab = list(fb)
        i = 0
        molecule = []
        while (i != len(tab)):
            if  fb[i].isupper():
                j = i + 1
                if i + 1 == len(tab) or fb[i+1].isupper():
                    molecule.append([abondances[fb[i]],1])
                    i += 1
                elif is_number(fb[i+1]):
                    nombre = ""
                    while is_number(fb[j]):
                        nombre += fb[j]
                        j += 1
                        if j >= len(tab):
                            break
                    molecule.append([abondances[fb[i]],int(nombre)])
                    
                elif fb[i+1].islower():
                    j += 1
                    if fb[i+2].isupper():
                        molecule.append([abondances[fb[i]+fb[i+1]],1])
                    elif is_number(fb[i+2]):
                        nombre = ""
                        while is_number(fb[j]):
                            nombre += fb[j]
                            j += 1
                            if j >= len(tab):
                                break
                        molecule.append([abondances[fb[i]+fb[i+1]],int(nombre)])
            i = j
        return molecule
#.............................................................................

"-------------------------------------------------------------"

"""Algorithme de tri pour la liste des résultats"""

#.............................................................................
#E         result, la liste de tout les résultats
#          t, la variable qui détermine le tri
#Action    Permet de trier les résultats finaux dans l'ordre décroissant
#S         new_result, la liste triée de tout les résultats
def triInsert(result,t):
    
    new_result = deepcopy(result)
    n = len(result)

    for i in range (1,n):
        x = new_result[i]
        j = i
        while ((j > 0) and new_result[j-1][t] > x[t]):
            new_result[j] = new_result[j-1]
            j = j-1
        new_result[j] = x

    return new_result
#.............................................................................

#.............................................................................
#E         result, la liste de tout les résultats
#Action    Passer d'une liste où la valeur la plus élevée est 100 à une liste où le total est 100
#S         new_result, la liste traitée de tout les résultats
def relatif_to_total(result):
    total = 0.
    for ligne in result:
        total += ligne[1]
    for ligne in result:
        ligne[1] = 100*ligne[1]/total
    return result
#.............................................................................

"-------------------------------------------------------------"

"""Récupération des informations du spectre"""

#.............................................................................
#E         chaine, variable de type '2.911e3'
#Action    Permet de transformer en float en prenant en compte la puissance de 10
#S         La valeur de la chaine en float 2911
def convertir_puissances(chaine):
    i = 0
    for caractere in chaine:
        if caractere == "e":
            return float(chaine[:i])*(10**float(chaine[i+1]))
        else:
            i += 1
    return float(chaine)
#.............................................................................

#.............................................................................
#E         filename,  le nom du fichier contenant le spectre.
#Action    Permet de récupérer les valeurs zommée d'un spectre depuis un fichier texte
#S         abondances,  un dictionnaire dont les indices sont les symboles chimiques des atomes
def upload_spectrum(filename="./../spectrum_list.txt"):
    try:
        with open(filename, encoding='utf-16') as f:
            tableau = f.read()
    except:
        with open(filename, "r") as f:
            tableau = f.read()
    f.close()
    tableau = tableau.split("\n")[3:]

    # On enlève d'abord tous les espaces
    for i in range(len(tableau)):
        ligne = tableau[i].split("\t")
        nouvelle_ligne = []
        for case in ligne:
            if case != '':
                nouvelle_ligne.append(case)
        tableau[i] = [convertir_puissances(x) for x in nouvelle_ligne]

    # Puis on récupère la zone zoomée
    i = 0
    while i < len(tableau):
        if len(tableau[i]) == 4:
            tableau[i] = tableau[i][2:]
            i += 1
        else:
            del tableau[i]
    return tableau
#.............................................................................