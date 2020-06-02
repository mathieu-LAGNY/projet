#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:41:25 2020

@author: mathieu
"""

"-------------------------------------------------------------"

"""Calcul du résultat selon l'algorithme des L3 Math"""

#.............................................................................
#E         n, le nombre d'expériences réalisées.
#          p, la probabilité de succès.
#Action    Permet d'éxécuter une loi binomiale
#S         ntok // ktok, le résultat de la loi binomiale
def binomial(n,k):
    if (0<=k<= n):
        ntok,ktok = 1,1
        for t in range(1,min(k,n-k)+1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0
#.............................................................................

#.............................................................................
#E         none
#Action    Permet de donner toutes les possibilités de calcul direct
#S         mass, la liste des masses
#          prob, la liste des probabilités
def possibilites():
    
    mass = []
    prob = []
    
    for H1 in range(int(H.nbr)+1):
     for C12 in range(int(C.nbr)+1):
      for O16 in range(int(O.nbr)+1):
       for O17 in range((int(O.nbr)-O16)+1):
        for N14 in range(int(N.nbr)+1):
         for S32 in range(int(S.nbr)+1):
          for S33 in range((int(S.nbr)-S32)+1):
           for S34 in range((int(S.nbr)-S32-S33)+1):
            for Cl35 in range(int(Cl.nbr)+1):
                    
                #Calcul des masses
                w = (H.iso[1][0]) * H1 + (H.iso[1][1]) * (int(H.nbr)-H1)
                w += (C.iso[1][0]) * C12 + (C.iso[1][1]) * (int(C.nbr)-C12)
                w += (O.iso[1][0]) * O16 + (O.iso[1][1]) * O17 + (O.iso[1][2]) * (int(O.nbr)-O16-O17)
                w += (N.iso[1][0]) * N14 + (N.iso[1][1]) * (int(N.nbr)-N14)
                w += (S.iso[1][0]) * S32 + (S.iso[1][1]) * S33 + (S.iso[1][2]) * S34 + (S.iso[1][3]) * (int(S.nbr)-S32-S33-S34)
                w += (Cl.iso[1][0]) * Cl35 + (Cl.iso[1][1]) * (int(Cl.nbr)-Cl35)
                
                #Calcul des probabilités                     
                p = binomial(int(H.nbr),H1)*(H.iso[0][0])**H1*(H.iso[0][1])**(int(H.nbr)-H1)
                p *= binomial(int(C.nbr),C12)*(C.iso[0][0])**C12*(C.iso[0][1])**(int(C.nbr)-C12)
                p *= binomial(int(O.nbr),O16)*binomial(int(O.nbr)-O16,O17)*(O.iso[0][0])**O16*(O.iso[0][1])**O17*(O.iso[0][2])**(int(O.nbr)-O16-O17)
                p *= binomial(int(N.nbr),N14)*(N.iso[0][0])**N14*(N.iso[0][1])**(int(N.nbr)-N14)
                p *= binomial(int(S.nbr),S32)*binomial(int(S.nbr)-S32,S33)*binomial(int(S.nbr)-S32-S33,S34)*(S.iso[0][0])**S32*(S.iso[0][1])**S33*(S.iso[0][2])**S34*(S.iso[0][3])**(int(S.nbr)-S32-S33-S34)
                p *= binomial(int(Cl.nbr),Cl35)*(Cl.iso[0][0])**Cl35*(Cl.iso[0][1])**(int(Cl.nbr)-Cl35)
               
                #Insertion des informations dans les listes
                if (w not in mass):
                    mass.append(w)
                    prob.append(p)
                else:
                    prob[mass.index(w)]+=p
                                        
    return mass,prob
#.............................................................................

#.............................................................................
#E         none
#Action    Permet de trier les résultats finaux
#S         result, la liste de tout les résultats
def calcul():
    
    mass,prob = possibilites()
    result = []
    
        
    try :
        if (int(opt.get()) == 0):
            arr = float(Earr1.get())
        elif (int(opt.get()) == 1):
            arr = float(Earr2.get())
    
        for i in range (len(mass)):
            maxi = max(prob)
            if ((prob[i]/maxi)*100 > arr):
                result.append([mass[i],prob[i],(prob[i]/maxi)*100])
    except :
        Lalertd = Label(F3d,text='Attention - Arrondi incorrect',font='Helvetica 15 bold',fg='red',bg='sky blue',padx=20,width=25) 
        Lalertd.grid(row=1,column=1,columnspan=2)
            
    return result
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
