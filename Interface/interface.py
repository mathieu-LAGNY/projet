#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:40:48 2020

@author: mathieu
"""
import matplotlib.pyplot as plt
import pylab
from functools import partial

import tkinter
from tkinter import ttk 
from tkinter import messagebox
from tkinter.filedialog import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import Main
from calcul_direct import calculdirect
from calcul_inverse import problemeinverse
import xls_management
import png_management

"-------------------------------------------------------------"

"""Fonction pour le tkinter - Direct"""


#.............................................................................
#E         none
#Action    Permet l'affichage de la fenêtre d'informations sur les isotopes
#S         none
def inf_aff():
    
    racine_abondance = tkinter.Tk()
    racine_abondance.title('Isotope Information')
    
    racine_abondance.bind('<Escape>', lambda e: racine_abondance.destroy())
    
        #.............................................................................
    #E         adresse du fichier contenant les abondances relatives
    #Action    Permet l'affichage des valeurs
    #S         none
    def afficher_document(filename="./../abondances/abondances.txt"):
        content = Main.upload_abondances(filename)
        
        def fenetre_atome(abondances,atome):

            tab_info = abondances[atome]
            
            racine_atome = tkinter.Tk()
            racine_atome.title(atome+' Information')
            
            def save_atome():
                i = 0
                total = 0
                for entry in tab_entry:
                    tab_info_relatif[i][0] = float(entry.get())
                    total +=  float(entry.get())
                    i += 1
                if total < 100.1 and total > 99.9:
                    tab_info = tab_info_relatif
                else:
                    fenetre = messagebox.showinfo("Incorrect argument","The sum of isotopic abundances must be equal to 100.")
                racine_atome.destroy()
            
            racine_atome.bind('<Escape>', save_atome)
            
            tab_info_relatif = Main.relatif_to_total(tab_info)
            
            lm = tkinter.Label(racine_atome,text='Isotope',padx=10,pady=10)
            lm.grid(row=1,column=1)
            
            lia = tkinter.Label(racine_atome,text='Isotopic Abundance',padx=10,pady=10)
            lia.grid(row=1,column=2)
            
            tab_entry = []
            
            for i in range (len(tab_info_relatif)):
                label = tkinter.Label(racine_atome,text=atome+str(round(tab_info_relatif[i][0])),padx=10)
                label.grid(row=i+2,column=1)
                
                entry = tkinter.Entry(racine_atome)
                entry.grid(row=i+2,column=2)
                entry.insert(0,str(tab_info_relatif[i][1]))
                
                tab_entry.append(entry)
            
            Bouton_validation = tkinter.Button(racine_atome,text='Validate',command=save_atome,padx=100)
            Bouton_validation.grid(row=len(tab_info_relatif)+3,columnspan=3)
            
        
        tableau = [["H","","","","","","","","","","","","","","","","","He"],\
                   ["Li","Be","","","","","","","","","","","B","C","N","O","F","Ne"],\
                   ["Na","Mg","","","","","","","","","","","Al","Si","P","S","Cl","Ar"],\
                   ["K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr"],\
                   ["Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe"],\
                   ["Cs","Ba","57-71","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn"],\
                   ["Fr","Ra","89-103","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Uut","Fl","Uup","Lv","Ts","Og"],\
                   ["","","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu"],\
                   ["","","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr"]]
        
        for i in range(len(tableau)):
            for j in range(len(tableau[i])):
                if tableau[i][j] != "":
                    Button(racine_abondance,text=tableau[i][j],command=partial(fenetre_atome,content,tableau[i][j]), width=2,height=1).grid(row=i, column=j)

    #.............................................................................
    
    def changer_document():
        filename = askopenfilename(initialdir="./../abondances",title="Select file",\
                                   filetypes=[('txt files','.txt'),('all files','.*')])
        if filename != ():
            afficher_document(filename)
            
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
    
    menu_abondance=tkinter.Menu(racine_abondance) # Creation du systeme de menu

    menu1_abondance=tkinter.Menu(menu_abondance, tearoff="0") # Creation du premier menu:
    menu_abondance.add_cascade(label="File", menu=menu1_abondance)

    menu1_abondance.add_command(label="Upload", command=changer_document)
    menu1_abondance.add_command(label="Save", command=enregistrer_document)
    
    racine_abondance.config(menu=menu_abondance)

    afficher_document()
    Bouton_validation = tkinter.Button(racine_abondance,text='Validate',command=enregistrer_document,padx=100)
    Bouton_validation.grid(row=12,columnspan=20,pady=10)
#.............................................................................

#.............................................................................
#E         none
#Action    Permet l'affichage du diagramme dans une fenêtre
#S         none   
def display_diag(result,formule_brute):
    
    source = Tk()
    source.title('Results Chart')
    
    fig, ax = plt.subplots()
    
    ax.set_title("Calcul direct de "+formule_brute)

    x = [result[i][0] for i in range (len(result))]
    height = [result[i][1] for i in range (len(result))]
    width = 0.02
    
    columns = plt.bar(x, height, width, color='blue')
    
    plt.xlim(min(x)-1,max(x)+1)
    plt.ylim(0,110)
    
    def autolabel(columns):
        """Attach a text label above each column in *columns*, displaying its height."""
        for column in columns:
            label = str(round(column.get_x(),2))+" ; "+str(round(column.get_height(),0))
            if round(column.get_height(),0) == 0:
                label = round(column.get_x(),2)
            ax.annotate('{}'.format(label),
                        xy=(column.get_x(), column.get_height()),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
            
    autolabel(columns)
        
    canvas = FigureCanvasTkAgg(fig,master=source)
    canvas.draw()
    
    toolbar = NavigationToolbar2Tk(canvas, source)
    toolbar.update()
    
    def on_key_press(event):
        key_press_handler(event, canvas, toolbar)
    
    canvas.mpl_connect("key_press_event", on_key_press)
    
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    
    source.mainloop()
#.............................................................................

#.............................................................................
#E         widget parent, formule brute de la molécule, les deux paramètres
#          secondaires du calcul direct, l'ordre de tri, et le tableau pour afficher les résultats
#Action    Permet de lancer la lecture, le calcul et l'affichage des résultats
#S         none
def execute_calcul_direct(racine, formule_brute, resolution, sensibilite, tri,  w_result):

    molecule = Main.lecture_FB(formule_brute)
      
    sensibilite = float(sensibilite)
    resolution = float(resolution)
    
    result = Main.triInsert(calculdirect(molecule,resolution,sensibilite),tri)
    
    for w in w_result:
        w.destroy()
    Ftab = tkinter.LabelFrame(racine,text='Results for '+formule_brute,padx=10,pady=10)
    Ftab.grid(row=5,column=1,columnspan=2,padx=10,pady=20)
    w_result.append(Ftab)
   
    lm = tkinter.Label(Ftab,text='Mass',padx=10,pady=10)
    lm.grid(row=1,column=1)
    w_result.append(lm)
    
    lri = tkinter.Label(Ftab,text='Relative intensity',padx=10,pady=10)
    lri.grid(row=1,column=2)
    w_result.append(lri)
    
    lnp = tkinter.Label(Ftab,text='Number of peaks',padx=10,pady=10)
    lnp.grid(row=1,column=3)
    w_result.append(lnp)
    
    for i in range (len(result)):
        for j in range (0,3):
            label = tkinter.Label(Ftab,text=result[i][j],padx=10)
            label.grid(row=i+2,column=j+1)
            w_result.append(label)
    
    menu1.delete(1)
    item1.delete(0)
    item1.delete(0)
    menu1.add_command(label="See Spectrogram", command=lambda : display_diag(result,formule_brute))
    item1.add_command(label=".xls file", command=lambda : save_spectre_xls(result))
    item1.add_command(label=".png file", command=lambda : save_spectre_png(result,formule_brute))
#.............................................................................

#.............................................................................
#E         widget parent, formule brute de la molécule, les deux paramètres
#          secondaires du calcul inverse, l'ordre de tri, et le tableau pour afficher les résultats
#Action    Permet de lancer la lecture, le calcul et l'affichage des résultats
#S         none
def execute_calcul_inverse(racine, formule_brute, oxygenes, spectre, resolution, sensibilite, tri, w_result):
    
    molecule = Main.lecture_FB(formule_brute)
      
    sensibilite = float(sensibilite)
    resolution = float(resolution)
    
    result,estimerreur = problemeinverse(molecule,oxygenes,spectre,resolution,sensibilite)
    result = Main.triInsert(result,tri)
    result = Main.relatif_to_total(result)

    for w in w_result:
        w.destroy()
    Ftab = tkinter.LabelFrame(racine,text='Results for '+formule_brute,padx=10,pady=10)
    Ftab.grid(row=5,column=1,columnspan=2,padx=10,pady=20)
    w_result.append(Ftab)
   
    lm = tkinter.Label(Ftab,text='Oxygen Mass',padx=10,pady=10)
    lm.grid(row=1,column=1)
    w_result.append(lm)
    
    lp = tkinter.Label(Ftab,text='Proportion',padx=10,pady=10)
    lp.grid(row=1,column=2)
    w_result.append(lp)
    
    for i in range (len(result)):
        for j in range (0,2):
            label = tkinter.Label(Ftab,text=result[i][j],padx=10)
            label.grid(row=i+2,column=j+1)
            w_result.append(label)

#.............................................................................

def save_spectre_xls(spectre):
    filename = asksaveasfilename(initialdir="./../",title="Save as xls file",\
                                 filetypes=[('xls files','.xls'),('all files','.*')])
    if filename != ():
        xls_management.export_xls(spectre,filename)
    
def save_spectre_png(spectre,formule_brute):
    filename = asksaveasfilename(initialdir="./../",title="Save as png file",\
                                 filetypes=[('png files','.png'),('all files','.*')])
    if filename != ():
        png_management.export_diag(spectre,filename,formule_brute)

#.............................................................................
    
def direct_tab(racine):
    Ftab = tkinter.LabelFrame(racine,text='Results for ',padx=10,pady=10)
    Ftab.grid_forget()
    w_result = []
    
    def appel_calcul_direct():
        execute_calcul_direct(racine, Efb.get(),Eres.get(),Esen.get(),tri.get(),w_result)
    # Frames de sélection #
    Fs1 = tkinter.LabelFrame(racine,text='Selection',padx=10,pady=10)
    Fs1.grid(row=4,column=1,columnspan=2,padx=10,pady=10)
    
    Lfb = tkinter.Label(Fs1,text='Molecular formula',padx=20)
    Lfb.grid(row=1,column=1)
    Efb = tkinter.Entry(Fs1)
    Efb.grid(row=1,column=2,columnspan=2,padx=20)
    
    Lres = tkinter.Label(Fs1,text='Resolution',padx=20) 
    Lres.grid(row=2,column=1)
    Eres = tkinter.Entry(Fs1)
    Eres.insert(0,'0.1')
    Eres.grid(row=2,column=2,columnspan=2,padx=20)
    
    Lsen = tkinter.Label(Fs1,text='Sensitivity',padx=20) 
    Lsen.grid(row=3,column=1)
    Esen = tkinter.Entry(Fs1)
    Esen.insert(0,'0.00001')
    Esen.grid(row=3,column=2,columnspan=2,padx=20)
    
    Bval = tkinter.Button(Fs1,text='Compute',command=appel_calcul_direct)
    Bval.grid(row=4,column=1)
    
    ######################################################
    
    # Partie de validation #
    F4d = tkinter.LabelFrame(racine,text='Validation',padx=10,pady=10)
    F4d.grid(row=6,column=1,columnspan=2,padx=10,pady=10)
    
    tri = tkinter.IntVar()
    Rom = tkinter.Radiobutton(F4d,text="Mass order",variable=tri,value=0,indicatoron=0,command=appel_calcul_direct,width=20)
    Rom.grid(row=1,column=1)
    Roi = tkinter.Radiobutton(F4d,text="Relative intensity order",variable=tri,value=1,indicatoron=0,command=appel_calcul_direct,width=20)
    Roi.grid(row=2,column=1)

#.............................................................................
    
def inverse_tab(racine):
    Ftab = tkinter.LabelFrame(racine,text='Results for ',padx=10,pady=10)
    Ftab.grid_forget()
    w_result = []
    
    def appel_calcul_inverse():
        spectre = Main.upload_spectrum(Espc.get())
        if spectre == []:
            fenetre = messagebox.showinfo("Missing or incorrect argument","You need to import a new spectrum")
            spectre = imp_spectre()
        oxygen = [int(element) for element in Eox.get().split(",")]
        execute_calcul_inverse(racine,Efb.get(),oxygen,spectre,Eres.get(),Esen.get(),tri.get(),w_result)
        
    def imp_spectre():
        Espc.delete(0,len(Espc.get()))
        filename = askopenfilename(initialdir="./../",title="Select file",\
                                   filetypes=[('txt files','.txt'),('all files','.*')])
        if filename != ():
            Espc.insert(0,filename)
    
    # Frames de sélection #
    Fs1 = tkinter.LabelFrame(racine,text='Selection',padx=10,pady=10)
    Fs1.grid(row=4,column=1,columnspan=2,padx=10,pady=10)
    
    Lfb = tkinter.Label(Fs1,text='Molecular formula',padx=20)
    Lfb.grid(row=1,column=1)
    Efb = tkinter.Entry(Fs1)
    Efb.grid(row=1,column=2,columnspan=2,padx=20)
    
    Lres = tkinter.Label(Fs1,text='Resolution',padx=20) 
    Lres.grid(row=2,column=1)
    Eres = tkinter.Entry(Fs1)
    Eres.insert(0,'0.1')
    Eres.grid(row=2,column=2,columnspan=2,padx=20)
    
    Lsen = tkinter.Label(Fs1,text='Sensitivity',padx=20) 
    Lsen.grid(row=3,column=1)
    Esen = tkinter.Entry(Fs1)
    Esen.insert(0,'0.00001')
    Esen.grid(row=3,column=2,columnspan=2,padx=20)
    
    Fox = tkinter.LabelFrame(Fs1,text='Oxygen enrichment',padx=10,pady=10)
    Fox.grid(row=4,column=1,columnspan=2,padx=10,pady=10)
    
    text = StringVar()
    
    text.set('You need to specify the number of oxygen of each "type" whose isotopic distributions are sought. For example, if you have an “unenriched” and an “enriched” oxygen, you must put 1 in the list of sought oxygen. If you have two oxygen enriched but possibly differently, you have to put 1.1 in the list of sought orygens. If we have three symmetric carboxyl functions whose two oxygen react differently to enrichment, it is necessary to put 3.3 in the list of sought oxygen.')
    msg = Message(Fox,textvariable=text, justify=CENTER, width=500)
    msg.grid(row=1,column=1,columnspan=3)
    
    Lox = tkinter.Label(Fox,text='Number of type of "enriched" oxygen') 
    Lox.grid(row=2,column=1)
    Eox = tkinter.Entry(Fox)
    Eox.insert(0,'1')
    Eox.grid(row=2,column=2,columnspan=2,padx=20)
    
    Espc = tkinter.Entry(Fs1)
    
    Bspectre = tkinter.Button(Fs1,text='Import new spectrum',command=imp_spectre)
    Bspectre.grid(row=5,column=1,columnspan=2)
    
    Bval = tkinter.Button(Fs1,text='Compute',command=appel_calcul_inverse)
    Bval.grid(row=6,column=1,columnspan=2)
    
    ######################################################
    
    # Partie de validation #
    F4d = tkinter.LabelFrame(racine,text='Validation',padx=10,pady=10)
    F4d.grid(row=6,column=1,columnspan=2,padx=10,pady=10)
    
    tri = tkinter.IntVar()
    Rom = tkinter.Radiobutton(F4d,text="Oxygen Mass",variable=tri,value=0,indicatoron=0,command=appel_calcul_inverse,width=20)
    Rom.grid(row=1,column=1)
    Roi = tkinter.Radiobutton(F4d,text="Proportion",variable=tri,value=1,indicatoron=0,command=appel_calcul_inverse,width=20)
    Roi.grid(row=2,column=1)
"-------------------------------------------------------------"

"""Mise en place du tkinter"""

######################################################

### Fenêtre principale ###
racine0 = tkinter.Tk()
racine0.title('Mass Spectrometer')

######################################################

# Menu #

sysdemenu0=tkinter.Menu(racine0) # Creation du systeme de menu

menu1=tkinter.Menu(sysdemenu0, tearoff="0") # Creation du premier menu:
sysdemenu0.add_cascade(label="File", menu=menu1)

# addition du premier item pour le second menu et leur sous-items associes
item1=tkinter.Menu(menu1, tearoff="0")
menu1.add_cascade(label="Save as", menu=item1)

menu1.add_command(label="See Spectrogram", state='disabled')

# addition des sous-items du premier item du second menu et leur commande associee
item1.add_command(label=".xls file", state='disabled')
item1.add_command(label=".png file", state='disabled')

menu2=tkinter.Menu(sysdemenu0, tearoff="0") # Creation du second menu
sysdemenu0.add_cascade(label="Options", menu=menu2)

menu2.add_command(label="Information on Isotopes", command=inf_aff)

racine0.config(menu=sysdemenu0)

######################################################

tabControl = ttk.Notebook(racine0)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

direct_tab(tab1)
inverse_tab(tab2)

tabControl.add(tab1, text='Calcul direct')
tabControl.add(tab2, text='Calcul inverse')

tabControl.grid() 

######################################################



"-------------------------------------------------------------"

"""Mise en place du tkinter"""

racine0.mainloop()

"-------------------------------------------------------------"