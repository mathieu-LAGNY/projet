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
#E         filename,  le nom du fichier contenant les abondances.
#Action    Permet de récupérer les valeurs des abondances isotopiques depuis un fichier texte
#S         abondances,  un dictionnaire dont les indices sont les symboles chimiques des atomes
def upload_abondances(filename="./../abondances/abondances.txt"):
    table = open(filename,"r")
    contenu = table.read().split("\n")
    abondances = {}
    
    for i in range(len(contenu)):
        
        #On récupère toutes les informations sur les atomes dans la table
        atom = contenu[i][:-2].split("=[[")
        
        #On recupère les informations sur les masses et indices
        tableau_couples = []
        ligne = atom[1].split("],[")
        for j in range (len(ligne)):
            couple = ligne[j].split(",")
            tableau_couples.append([float(couple[0]),float(couple[1])])
        
        #On sauvegarde les informations 
        abondances[atom[0]] = tableau_couples
    table.close()
    return abondances
#.............................................................................

"-------------------------------------------------------------"

"""Fonctions de lecture d'une formule brute"""

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
#Action    Permet de trier les résultats finaux
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