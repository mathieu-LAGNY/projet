#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:40:48 2020

@author: mathieu
"""
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import *
import Main
from calcul_direct import calculdirect
import xls_management
import png_management
import matplotlib.pyplot as plt
import pylab

"-------------------------------------------------------------"

"""Fonction pour le tkinter - Direct"""


#.............................................................................
#E         none
#Action    Permet l'affichage de la fenêtre d'informations sur les isotopes
#S         none
def inf_aff():
    
    racine_abondance = tkinter.Tk()
    racine_abondance.title('Isotope Information')

    txt_abondance=tkinter.Text(racine_abondance) # prevoit une place pour l'affichage des textes
    txt_abondance.pack()
  
    #.............................................................................
    #E         Une chaîne de caractères
    #Action    Permet d'afficher des valeurs
    #S         none    
    def ecran(var):
        txt_abondance.insert(tkinter.END, var)
    #.............................................................................
    
    #.............................................................................
    #E         none
    #Action    Permet l'affichage des valeurs
    #S         none 
    def afficher_document():
        filename = askopenfilename(initialdir="./../abondances",title="Select file",\
                                   filetypes=[('txt files','.txt'),('all files','.*')])
        fichier = open(filename, "r")
        content = fichier.read()
        ecran(content)
        fichier.close()
    #.............................................................................
    
    #.............................................................................
    #E         none
    #Action    Permet l'enregistrement des nouvelles valeurs dans un fichier texte
    #S         none
    def enregistrer_document():
        filename = asksaveasfilename(initialdir="./../abondances",title="Select file",\
                                     filetypes=[('txt files','.txt'),('all files','.*')])
        fichier = open(filename, "w")
        fichier.write(txt_abondance.get("1.0",END))
        fichier.close()
        racine_abondance.destroy()
    #.............................................................................
    
    afficher_document()
    Bouton_validation = tkinter.Button(racine_abondance,text='Valider',command=enregistrer_document,padx=100)
    Bouton_validation.pack()
#.............................................................................

#.............................................................................
#E         none
#Action    Permet l'affichage du diagramme dans une fenêtre
#S         none   
def display_diag(result):
    
    diag = Tk()
    diag.title('Diagramme des résultats')
    
    fig = plt.figure()

    x = [result[i][0] for i in range (len(result))]
    height = [result[i][1] for i in range (len(result))]
    width = 0.02
    BarName = [str(result[i][0]) for i in range (len(result))]
    
    plt.bar(x, height, width, color='blue')
    
    plt.xlim(min(x)-0.2,max(x)+0.2)
    plt.ylim(0,max(height)+0.1)
    
    pylab.xticks(x, BarName, rotation=40)
    
    canvas = FigureCanvasTkAgg(fig,master=diag)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=1)
    
    diag.mainloop()
#.............................................................................

#.............................................................................
#E         none
#Action    Permet de lancer la lecture, le calcul et l'affichage des résultats
#S         none    print(calculdirect(lecture_FB("C257H383O77N65S6"),0.1,0.1))
def valid():
    
    if Efb.get() != "":
        molecule = Main.lecture_FB(Efb.get())

        abondances = Main.upload_abondances()
      
        result = Main.triInsert(calculdirect(molecule,0.1,0.1),int(tri.get()))
   
        Ftab = tkinter.LabelFrame(direct,text='Résultat pour '+Efb.get(),padx=10,pady=10)
        Ftab.grid(row=5,column=1,columnspan=2,padx=10,pady=20)
        lm = tkinter.Label(Ftab,text='Masse',padx=10,pady=10)
        lm.grid(row=1,column=1)
        lp = tkinter.Label(Ftab,text='Probabilité',padx=10,pady=10)
        lp.grid(row=1,column=2)
    
        for i in range (len(result)):
            for j in range (0,2):
                label = tkinter.Label(Ftab,text=result[i][j],padx=10)
                label.grid(row=i+2,column=j+1)
    
        Fexp1 = tkinter.LabelFrame(direct,text='Exportation en .xls',padx=10,pady=10)
        Fexp1.grid(row=7,column=1,padx=10,pady=20)
        txls = tkinter.Label(Fexp1,text='Entrer le nom du fichier') 
        txls.grid(row=1,column=1,columnspan=2)
        exls = tkinter.Entry(Fexp1)
        exls.grid(row=2,column=1)
        bxls = tkinter.Button(Fexp1,text='Valider',command = lambda: xls_management.export_xls(result,exls.get()))
        bxls.grid(row=2,column=2)
    
        Fexp2 = tkinter.LabelFrame(direct,text='Exportation en .png', padx=10, pady=10)
        Fexp2.grid(row=7,column=2,padx=10,pady=20)
        tpng = tkinter.Label(Fexp2,text='Entrer le nom du fichier') 
        tpng.grid(row=1,column=1,columnspan=2)
        epng = tkinter.Entry(Fexp2)
        epng.grid(row=2,column=1)
        bpng = tkinter.Button(Fexp2,text='Valider',command = lambda: png_management.export_diag(result,epng.get()))
        bpng.grid(row=2,column=2)
        spng = tkinter.Button(Fexp2,text='Voir',command = lambda: display_diag(result),width=20)
        spng.grid(row=3,column=1,columnspan=2,pady=5)
#.............................................................................

"-------------------------------------------------------------"

"""Mise en place du tkinter - Direct"""

######################################################

### Fenêtre pour la partie <Direct> ###
direct = tkinter.Tk()
direct.title('Spectromètre de masse - Direct')

######################################################

######################################################

# Frame des options #
F2d = tkinter.LabelFrame(direct,text='Option',padx=10,pady=10)
F2d.grid(row=2,column=1,columnspan=2)

Binf = tkinter.Button(F2d,text='Informations sur les Isotopes',command=inf_aff)
Binf.grid(row=3,column=1)

######################################################

# Frames de sélection #
Fs1 = tkinter.LabelFrame(direct,text='Sélection',padx=10,pady=10)
Fs1.grid(row=4,column=1,columnspan=2,padx=10,pady=10)

Lfb = tkinter.Label(Fs1,text='Formule brute',padx=20)
Lfb.grid(row=1,column=1)
Efb = tkinter.Entry(Fs1)
Efb.grid(row=1,column=2,columnspan=2,padx=20)

Larr1 = tkinter.Label(Fs1,text='Quantité minimale',padx=20) 
Larr1.grid(row=2,column=1)
Earr1 = tkinter.Entry(Fs1)
Earr1.insert(0,'0.0001')
Earr1.grid(row=2,column=2,columnspan=2,padx=20)

Bval = tkinter.Button(Fs1,text='Valider',command=valid)
Bval.grid(row=3,column=1)

######################################################

# Partie de validation #
F4d = tkinter.LabelFrame(direct,text='Validation',padx=10,pady=10)
F4d.grid(row=6,column=1,columnspan=2,padx=10,pady=10)

tri = tkinter.IntVar()
Rom = tkinter.Radiobutton(F4d,text="Ordre des Masses",variable=tri,value=0,indicatoron=0,command=valid,width=20)
Rom.grid(row=1,column=1)
Roi = tkinter.Radiobutton(F4d,text="Ordre des Probabilités",variable=tri,value=1,indicatoron=0,command=valid,width=20)
Roi.grid(row=2,column=1)

######################################################

"-------------------------------------------------------------"

"""Mise en place du tkinter"""

direct.mainloop()

"-------------------------------------------------------------"