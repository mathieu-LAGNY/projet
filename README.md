# projet

Le fichier de code central qui fait tourner le programme est interface.py.

Pour faire une version standalone, j'ai utilisé cx_Freeze avec le fichier setup.py. 
Pour l'utiliser, il faut lancer la commande "python setup.py build" dans le répertoire Interface. 
Un dossier "build" se trouvera ensuite dans ce répertoire. 
Dans le dossier "build", il faudra copier le repertoire "abondances" qui contient un petit fichier texte pour faire fonctionner la version actuelle du programme. 
Il est nécessaire d'avoir une installation de python avec tout les modules nécessaires pour chaque système d'exploitation pour lequel on souhaite faire une version standalone. Jusqu'ici, seuls une version ubuntu et windows 10 ont été réalisées. 


# Bibliothèques python utilisées

* matplotlib
* tkinter
* pylab
* openpyxl
* copy
* math

# Mise en place

Pour pouvoir continuer le programme, une installation de python avec les bons modules est nécessaire.
Ma version de Python est la 3.6.9, mais il est fortement possible que cela fonctionne avec une autre version plus récente. Les modules modules utilisés sont indiqués ci-dessus, je les ai installés avec leur version la plus récente (entre avril et juillet 2020).
Certains modules comme math seront surement installés dans votre disstribution de python, pour installer les autres modules, je ne peux que vous encourager à aller chercher les sources officielles et à vous fier à leurs consignes d'installation. En cas de problème, je vous conseille de chercher sur google, quelqu'un a sans doute eu le même problème que vous auparavant et la réponse aura de bonne chance d'être dans les premiers résultats.

Je recommande de télécharger les sources complètes du programme et de tenter de lancer avec python le programme interface.py dans le dossier interface. Votre interpréteur vous indiquera quels modules manquent le cas échéant.

# Structure

Le dossier abondance contient le fichier des abondances naturelles. Le dossier interface contient tout le code. Les nom des fichiers python sont explicites. Le fichier texte TO DO.txt contient mes petites notes prises pendant les réunions.

# Pour le futur

Pour ajouter des oxygènes suplémentaires, je pense qu'il faudrait les ajouter dans le fichier des abondances naturelles avec une abondance de 0.0 pour faciliter la vie des utilisateurs, cependant, toutes les opérations relatives à ce fichier telles que l'importation, l'utilisation des données qu'il contient, à la fois dans l'interface et dans les calculs doivent être revues pour s'assurer que cela ne procure aucun trouble.

Pour le calcul inverse, je pense qu'il pourrait être judicieux de faire une liste à puces contenant tout les choix possibles, et de modifier la transmission au calcul en accordance.

# Enfin

En cas de problème ou de doute, n'hésitez pas à me contacter par mail : m.lagny@laposte.net
