# projet

Le fichier de code central qui fait tourner le programme est interface.py.

Pour faire une version standalone, j'ai utilisé cx_Freeze avec le fichier setup.py. 
Pour l'utiliser, il faut lancer la commande "python setup.py build" dans le répertoire Interface. 
Un dossier "build" se trouvera ensuite dans ce répertoire. 
Dans le dossier "build", il faudra copier le repertoire "abondances" qui contient un petit fichier texte pour faire fonctionner la version actuelle du programme. 

# Bibliothèques python utilisées

* matplotlib
* tkinter
* pylab
* openpyxl
* copy
* math
