#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:36:14 2020

@author: mathieu
"""
from calcul_direct import *
from copy import deepcopy
import numpy as np

O = [[15.99491461956, 100.0], [16.9991317, 0.03809256493278667], [17.999161, 0.20549936345319125]]

def deresolution(K,resolution):
#   print('appel de deresolution')
    S=TriMasse(K)
    Lng=len(S)-1
    for i in range(len(S)-1):
        indice=Lng-i
        if S[indice][0]-S[indice-1][0]<resolution:
#        on calcule (en deux étapes!) la masse du couple regroupé
#        (en tenant compte des probabilités respectives)
            masseponderee=(S[indice][1]*S[indice][0]+S[indice-1][1]*S[indice-1][0])
            probatotale=S[indice][1]+S[indice-1][1]
            massemoyenne=masseponderee/probatotale
#        et on réduit notre liste:
            S=S[0:indice-1]+[[massemoyenne,probatotale]]+S[indice+1:]
    return TriMasse(S)

def multimatricialisation(L,k):
    h=len(L)
#    MM=matrix(RDF,k*h,k)
    MM=np.zeros((k*h,k))
#    print(k*h,k)
    for i in range(h):
        for j in range(k):
#            print(k*i+j,j)
#            MM[k*i+j,j]=L[i][1]
            MM[k*i+j][j]=L[i][1]
    return(MM)

def TrisimpleCroissant(L):
    for i in range(1,len(L)):
        if L[i]<L[0]:
            L=[L[i]]+L[0:i]+L[i+1:]
        else:
            j=i-1
            while L[i]<L[j]:
                j=j-1
            L=L[0:j+1]+[L[i]]+L[j+1:i]+L[i+1:]
    return(L)

def calculmasses(L,M):
    N=[]
    Lordonnee=TriMasse(L)
    Mordonnee=TrisimpleCroissant(M)
    for i in range(len(Lordonnee)):
        for j in range(len(Mordonnee)):
            N.append([Lordonnee[i][0]+Mordonnee[j],Lordonnee[i][1]])
    return N

def matrix_from_rows(matrice,ordre):
    result = []
    for i in ordre:
        result.append(matrice[i])
    return result

def reordonnancementSuivi(L,MM):
#    P=[0..len(L)-1]
    P=[i for i in range(len(L))]
    for i in range(1,len(L)):
        if L[i]<L[0]:
            L=[L[i]]+L[0:i]+L[i+1:]
            P=[P[i]]+P[0:i]+P[i+1:]
        else:
            j=i-1
            while L[i]<L[j]:
                j=j-1
            L=L[0:j+1]+[L[i]]+L[j+1:i]+L[i+1:]
            P=P[0:j+1]+[P[i]]+P[j+1:i]+P[i+1:]
#    return(L,MM.matrix_from_rows(P))
    return(L,matrix_from_rows(MM,P))

def regroupementmasses(L,MM,resolution):
#    MMM=copy(MM)
    MMM=deepcopy(MM)
    S=L
    Lng=len(S)-1
    for i in range(Lng):
        indice=Lng-i
        if S[indice][0]-S[indice-1][0]<resolution:
#        on calcule (en deux étapes!) la masse du couple regroupé
#        (en tenant compte des probabilités respectives)
            masseponderee=(S[indice][1]*S[indice][0]+S[indice-1][1]*S[indice-1][0])
            probatotale=S[indice][1]+S[indice-1][1]
            massemoyenne=masseponderee/probatotale
#        et on réduit notre liste:
            S=S[0:indice-1]+[[massemoyenne,probatotale]]+S[indice+1:]
#        et après, on fait suivre les opérations sur les lignes de MMM
            V=MMM[indice]+MMM[indice-1]
#            listeintermediaire=[0..indice-1]+[indice+1..MMM.nrows()]
            listeintermediaire=[i for i in range(indice)]+[i for i in range(indice+1,len(MMM)+1)]
#            MMM=MMM.matrix_from_rows(listeintermediaire[:-1])
            MMM=matrix_from_rows(MMM,listeintermediaire[:-1])
            MMM[indice-1]=V
    return S,MMM

def secondmembre(L,RE,resolution):
    N=deresolution(RE,resolution)
#    print('N=',N)
    S=[0]*len(L)
    for j in range(len(N)):
#        print('j=',j)
        k=len(L)-1
        c=True
        while c and k>=0:
#            print('k=',k)
            if abs(N[j][0]-L[k][0])<resolution:
                S[k]=N[k][1]
                c=False
            k=k-1
        if c:
            print("pic",N[j],"non reconnu")
    return S

def problemeinverse(AU,MES,resolution,sensibilite):
    #etape 1°
    Base=calculdirect(AU, resolution, sensibilite)
    #print('etape1: Base=',Base)
    #etape 2°
    matrice1=multimatricialisation(Base,3)
    #print('etape2OK')
    #etape 3°
    masses=[]
    for i in range(3):
        masses.append(O[i][0])
    listemasses1=calculmasses(Base,masses)
    #print('etape3: listemasses1=',listemasses1)
    #etape 4°
    listemasses2,matrice2=reordonnancementSuivi(listemasses1,matrice1)
    #print('etape4: listemasses2=',listemasses2)
    #etape 5°
    listemasses3,matrice3=regroupementmasses(listemasses2,matrice2,resolution)
    #print('etape5: listemasses3:',listemasses3)
    #etape 6°
    image=secondmembre(listemasses3,MES,resolution)
    #print('etape6: image=',image)
    #etape 7°,1 On calcule des ''probas'' pour l'oxygène inconnu
    #print(matrice3)
#    transposee=matrice3.transpose()
    transposee=np.array(matrice3).transpose()
#    matricecarree=transposee*matrice3
    matricecarree=np.dot(transposee,matrice3)
#    solution=matricecarree.inverse()*transposee*vector(image)
    solution=np.dot(np.dot(np.linalg.inv(matricecarree),transposee),np.array(image).reshape(-1,1))
#    resultat=(100/solution.norm(infinity))*solution
    resultat=(100/max([abs(valeur) for valeur in solution]))*solution
    #print('etape7premiermorceau: resultat=',resultat)
    sortie=[]
    for i in range(len(resultat)):
#        sortie.append([masses[i],resultat[i]])
        sortie.append([masses[i],float(resultat[i])])
    #print('etape7deuxiemepartie: sortie=',sortie)
    #etape 8° ATTENTION A LA NORMALISATION:BASE100!!!!!
#    imageapprochee1=matrice3*solution
    imageapprochee1=np.dot(matrice3,solution)
#    imageapprochee2=(100/imageapprochee1.norm(infinity))*imageapprochee1
    imageapprochee2=(100/max([abs(valeur) for valeur in imageapprochee1]))*imageapprochee1
#    print(imageapprochee2)
#    imagevecteur=vector(image)
    imagevecteur=np.array(image).reshape(-1,1)
#    imagevecteurnormalisee=(100/imagevecteur.norm(infinity))*imagevecteur
    imagevecteurnormalisee=(100/max([abs(valeur) for valeur in imagevecteur]))*imagevecteur
#    estimerreur=(imageapprochee2-imagevecteurnormalisee).norm()
    estimerreur=abs(imageapprochee2-imagevecteurnormalisee)
#    return sortie,estimerreur
    return sortie,[float(valeur) for valeur in estimerreur]

molecule = [[[[12.0, 100.0], [13.0033548378, 1.0815728292732234]], 13], [[[1.00782503207, 100.0], [2.0141017778, 0.011501322652104991]], 17], [[[15.99491461956, 100.0], [16.9991317, 0.03809256493278667], [17.999161, 0.20549936345319125]], 1]]
resolution = 0.1
sensibilite = 0.00001
spectre = [[205.12285478431, 100.0, 1], [206.12625406684236, 14.332154395503267, 3], [207.1288872036823, 1.3617948228817307, 5], [208.1315029099693, 0.09656128181254368, 4], [209.13389630065876, 0.0038631215712527202, 2]]
sortie,estimerreur = problemeinverse(molecule,spectre,resolution,sensibilite)

print(sortie)