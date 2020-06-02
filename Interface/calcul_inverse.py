#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:36:14 2020

@author: mathieu
"""

def multimatricialisation(L,k):
    h=len(L)
    MM=matrix(RDF,k*h,k)
#    print(k*h,k)
    for i in range(h):
        for j in range(k):
#            print(k*i+j,j)
            MM[k*i+j,j]=L[i][1]
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

def reordonnancementSuivi(L,MM):
    P=[0..len(L)-1]
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
    return(L,MM.matrix_from_rows(P))

def regroupementmasses(L,MM,resolution):
    MMM=copy(MM)
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
            listeintermediaire=[0..indice-1]+[indice+1..MMM.nrows()]
            MMM=MMM.matrix_from_rows(listeintermediaire[:-1])
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
    transposee=matrice3.transpose()
    matricecarree=transposee*matrice3
    solution=matricecarree.inverse()*transposee*vector(image)
    resultat=(100/solution.norm(infinity))*solution
    #print('etape7premiermorceau: resultat=',resultat)
    sortie=[]
    for i in range(len(resultat)):
        sortie.append([masses[i],resultat[i]])
    #print('etape7deuxiemepartie: sortie=',sortie)
    #etape 8° ATTENTION A LA NORMALISATION:BASE100!!!!!
    imageapprochee1=matrice3*solution
    imageapprochee2=(100/imageapprochee1.norm(infinity))*imageapprochee1
    print(imageapprochee2)
    imagevecteur=vector(image)
    imagevecteurnormalisee=(100/imagevecteur.norm(infinity))*imagevecteur
    estimerreur=(imageapprochee2-imagevecteurnormalisee).norm()
    return sortie,estimerreur