# projet

Le fichier de code central qui fait tourner le programme est interface.py.

Pour faire une version standalone, j'ai utilisé cx_Freeze avec le fichier setup.py. 
Pour l'utiliser, il faut lancer la commande "python setup.py build" dans le répertoire Interface. 
Un dossier "build" se trouvera ensuite dans ce répertoire. 
Dans le dossier "build", il faudra copier le repertoire "abondances" qui contient un petit fichier texte pour faire fonctionner la version actuelle du programme. 

# setup.py

Jusqu'à la ligne 20 se trouve le code que j'ai utilisé pour la version Ubuntu qui fonctionne.
La suite contient différentes méthodes expérimentée pour arriver à le faire marcher sous windows, mais pour l'instant rien ne marche.

# Bibliothèques python utilisées

* matplotlib
* tkinter
* pylab
* openpyxl
* copy
* math
