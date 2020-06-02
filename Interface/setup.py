#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:07:25 2020

@author: mathieu
"""

"""Fichier d'installation de notre script salut.py."""
"""
from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "test",
    version = "0.5",
    description = "description interface",
    executables = [Executable("interface.py")],
)

from cx_Freeze import setup, Executable  
import os.path  #Permet d'éviter une erreur de type "KeyError: TCL_LIBRARY"
import sys 
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__)) 
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6') 
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6') 
options = {
     'build_exe': {
         'include_files':[
             os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
             os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
          ],
     },}  #Si vous souhaitez pouvoir exporter sur un autre système d'exploitation, ces lignes sont nécessaires. 
base = None  
if sys.platform == "win32":
     base = "Win32GUI"  #Fichier que l'on souhaite inclure dans le dossier de l'exécutable 
target = Executable(
     script = "interface.py",
     base = base)  
setup( name = "Interface",   version = "0.1" , description = "description" ,  executables = [target])"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
#Icone sous Windows: il faut:
#=> un xxx.ico pour integration dans le exe, avec "icon=xxx.ico"
#=> un xxx.png pour integration avec PyQt4 + demander la recopie avec includefiles.
import sys, os
from cx_Freeze import setup, Executable
#############################################################################
# preparation des options
# chemins de recherche des modules
# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
path = sys.path
# options d'inclusion/exclusion des modules
includes = []  # nommer les modules non trouves par cx_freeze
excludes = []
packages = ["numpy","scipy","matplotlib"]  # nommer les packages utilises
#packages = ["matplotlib.backends.backend_tkagg", "tkinter", "tkinter.filedialog", "scipy.sparse.csgraph._validation",  "scipy.special._ufuncs_cxx"]
# copier les fichiers non-Python et/ou repertoires et leur contenu:

includefiles = []
if sys.platform == "win32":
    pass
    # includefiles += [...] : ajouter les recopies specifiques à Windows
elif sys.platform == "linux2":
    pass
    # includefiles += [...] : ajouter les recopies specifiques à Linux
else:
    pass
    # includefiles += [...] : cas du Mac OSX non traite ici
# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]
# niveau d'optimisation pour la compilation en bytecodes
optimize = 0
# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = True
# construction du dictionnaire des options
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes,
           "optimize": optimize,
           "silent": silent
           }
# pour inclure sous Windows les dll system de Windows necessaires
if sys.platform == "win32":
    options["include_msvcr"] = True
#############################################################################
# preparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # pour application graphique sous Windows
    #base = "Console" # pour application en console sous Windows
icone = None
if sys.platform == "win32":
    icone = "icone.ico"
cible_1 = Executable(
    script="interface.py",
    base=base,
    #icon=icone
    )
#############################################################################
# creation du setup
setup(
    name="monprogramme",
    version="1.00",
    description="descriptiondemonprogramme",
    author="mathieu",
    options={"build_exe": options},
	executables=[cible_1]
    )