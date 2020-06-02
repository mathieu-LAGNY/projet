import tkinter
import pickle
from tkinter.filedialog import *

racine0=tkinter.Tk()

texte0=tkinter.Text(racine0) # prevoit une place pour l'affichage des textes
texte0.pack()
  
def ecran(var): # fonction servant a l'affichage des textes:
  texte0.insert(tkinter.END, var)
  
def afficher_document():
    filename = askopenfilename(title="Ouvrir votre document",filetypes=[('txt files','.txt'),('all files','.*')])
    fichier = open(filename, "r")
    content = fichier.read()
    ecran(content)
    fichier.close()

sysdemenu0=tkinter.Menu(racine0) # Creation du systeme de menu

menu1=tkinter.Menu(sysdemenu0, tearoff="0") # Creation du premier menu:
sysdemenu0.add_cascade(label="Menu 1", menu=menu1)

# addition des deux items pour le premier menu et leur commande associee
menu1.add_command(label="Credit", command=lambda: ecran('Credit: www.jchr.be\n'))
menu1.add_command(label="Quitter", command=racine0.destroy)

menu2=tkinter.Menu(sysdemenu0) # Creation du second menu
sysdemenu0.add_cascade(label="Menu 2", menu=menu2)

# addition du premier item pour le second menu et leur sous-items associes
item1=tkinter.Menu(menu2)
menu2.add_cascade(label="Item 1", menu=item1)

# addition des sous-items du premier item du second menu et leur commande associee
item1.add_command(label="Action 1", command=afficher_document)
item1.add_command(label="Action 2", command=lambda: ecran('Item 1 / Action 2\n'))

item2=tkinter.Menu(menu2) # addition du second item pour le second menu et leur sous-items associes
menu2.add_cascade(label="Item 2", menu=item2)

# addition des sous-items du second item du second menu et leur commande associee
item2.add_command(label="Action 1", command=lambda: ecran('Item 2 / Action 1\n'))
item2.add_command(label="Action 2", command=lambda: ecran('Item 2 / Action 2\n'))
item2.add_command(label="Action 3", command=lambda: ecran('Item 2 / Action 3\n'))
racine0.config(menu=sysdemenu0)
racine0.mainloop()



#Label(fenetre, text=content).pack(padx=10, pady=10)