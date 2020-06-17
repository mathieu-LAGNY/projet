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
        content = Main.upload_abondances(filename)
        ecran(content)
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
#Action    Permet l'importation d'un spectre
#S         none
def imp_spectre():
    
    filename = askopenfilename(initialdir="./../",title="Select file",\
                               filetypes=[('txt files','.txt'),('all files','.*')])
    print(filename)
    

    return 0
#.............................................................................

#.............................................................................
#E         none
#Action    Permet l'affichage du diagramme dans une fenêtre
#S         none   
def display_diag(result):
    
    diag = Tk()
    diag.title('Results Chart')
    
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
#S         Renvoie le Widget contenant le résultat    print(calculdirect(lecture_FB("C257H383O77N65S6"),0.1,0.1))
def valid():
    
    abondances = Main.upload_abondances()

    molecule = Main.lecture_FB(Efb.get())
      
    sensibilite = float(Esen.get())
    resolution = float(Eres.get())
    
    result = Main.triInsert(calculdirect(molecule,sensibilite,resolution),int(tri.get()))
    
    for w in w_result:
        w.destroy()
    Ftab = tkinter.LabelFrame(racine0,text='Results for '+Efb.get(),padx=10,pady=10)
    Ftab.grid(row=5,column=1,columnspan=2,padx=10,pady=20)
    w_result.append(Ftab)
   
    lm = tkinter.Label(Ftab,text='Mass',padx=10,pady=10)
    lm.grid(row=1,column=1)
    w_result.append(lm)
    
    lp = tkinter.Label(Ftab,text='Relative intensity',padx=10,pady=10)
    lp.grid(row=1,column=2)
    w_result.append(lp)
    
    for i in range (len(result)):
        for j in range (0,2):
            label = tkinter.Label(Ftab,text=result[i][j],padx=10)
            label.grid(row=i+2,column=j+1)
            w_result.append(label)
    
    item1.delete(0)
    item1.delete(0)
    item1.add_command(label=".xls file", command=lambda : save_spectre_xls(result))
    item1.add_command(label=".png file", command=lambda : save_spectre_png(result))
#.............................................................................

def save_spectre_xls(spectre):
    filename = asksaveasfilename(initialdir="./../",title="Save as xls file",\
                                 filetypes=[('xls files','.xls'),('all files','.*')])
    xls_management.export_xls(spectre,filename)
    
def save_spectre_png(spectre):
    filename = asksaveasfilename(initialdir="./../",title="Save as png file",\
                                 filetypes=[('png files','.png'),('all files','.*')])
    png_management.export_diag(spectre,filename)

"-------------------------------------------------------------"

"""Mise en place du tkinter - Direct"""

######################################################

### Fenêtre principale ###
racine0 = tkinter.Tk()
racine0.title('Mass Spectrometer')

######################################################

# Menu #

sysdemenu0=tkinter.Menu(racine0) # Creation du systeme de menu

menu1=tkinter.Menu(sysdemenu0, tearoff="0") # Creation du premier menu:
sysdemenu0.add_cascade(label="File", menu=menu1)

# addition des deux items pour le premier menu et leur commande associee
menu1.add_command(label="Import spectrum", command=valid)

menu2=tkinter.Menu(sysdemenu0) # Creation du second menu
sysdemenu0.add_cascade(label="Menu 2", menu=menu2)

# addition du premier item pour le second menu et leur sous-items associes
item1=tkinter.Menu(menu1, tearoff="0")
menu1.add_cascade(label="Save as", menu=item1)

# addition des sous-items du premier item du second menu et leur commande associee
item1.add_command(label=".xls file", state='disabled')
item1.add_command(label=".png file", state='disabled')

item2=tkinter.Menu(menu2) # addition du second item pour le second menu et leur sous-items associes
menu2.add_cascade(label="Item 2", menu=item2)

# addition des sous-items du second item du second menu et leur commande associee
item2.add_command(label="Action 1", command=valid)
item2.add_command(label="Action 2", command=valid)
item2.add_command(label="Action 3", command=valid)
racine0.config(menu=sysdemenu0)

######################################################

# Frame des options #
F2d = tkinter.LabelFrame(racine0,text='Option',padx=10,pady=10)
F2d.grid(row=2,column=1,columnspan=2)

Binf = tkinter.Button(F2d,text='Information on Isotopes',command=inf_aff)
Binf.grid(row=3,column=1)

######################################################

Ftab = tkinter.LabelFrame(racine0,text='Results for ',padx=10,pady=10)
Ftab.grid_forget()
w_result = []

######################################################

# Frames de sélection #
Fs1 = tkinter.LabelFrame(racine0,text='Selection',padx=10,pady=10)
Fs1.grid(row=4,column=1,columnspan=2,padx=10,pady=10)

Lfb = tkinter.Label(Fs1,text='Molecular formula',padx=20)
Lfb.grid(row=1,column=1)
Efb = tkinter.Entry(Fs1)
Efb.grid(row=1,column=2,columnspan=2,padx=20)

Lsen = tkinter.Label(Fs1,text='Sensibility (or sensitivity ?)',padx=20) 
Lsen.grid(row=2,column=1)
Esen = tkinter.Entry(Fs1)
Esen.insert(0,'0.1')
Esen.grid(row=2,column=2,columnspan=2,padx=20)

Lres = tkinter.Label(Fs1,text='Resolution',padx=20) 
Lres.grid(row=3,column=1)
Eres = tkinter.Entry(Fs1)
Eres.insert(0,'0.00001')
Eres.grid(row=3,column=2,columnspan=2,padx=20)

Bval = tkinter.Button(Fs1,text='Compute',command=valid)
Bval.grid(row=4,column=1)

######################################################

# Partie de validation #
F4d = tkinter.LabelFrame(racine0,text='Validation',padx=10,pady=10)
F4d.grid(row=6,column=1,columnspan=2,padx=10,pady=10)

tri = tkinter.IntVar()
Rom = tkinter.Radiobutton(F4d,text="Mass order",variable=tri,value=0,indicatoron=0,command=valid,width=20)
Rom.grid(row=1,column=1)
Roi = tkinter.Radiobutton(F4d,text="Relative intensity order",variable=tri,value=1,indicatoron=0,command=valid,width=20)
Roi.grid(row=2,column=1)

######################################################

"-------------------------------------------------------------"

"""Mise en place du tkinter"""

racine0.mainloop()

"-------------------------------------------------------------"