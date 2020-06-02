#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:41:57 2020

@author: mathieu
"""
import pylab
import matplotlib.pyplot as plt

"""Exportation en png"""

#.............................................................................
#E         result, la liste de tout les résultats
#          name, le nom du fichier à exporter
#Action    Permet d'exporter les résultats sur un graphes en format png
#S         none
def export_diag(result,name):
    
    fig = plt.figure()

    x = [result[i][0] for i in range (len(result))]
    height = [result[i][1] for i in range (len(result))]
    width = 0.02
    BarName = [str(result[i][0]) for i in range (len(result))]
    
    plt.bar(x, height, width, color='blue')
    
    plt.xlim(min(x)-0.2,max(x)+0.2)
    plt.ylim(0,max(height)+0.1)
    
    plt.title(name)
    
    pylab.xticks(x, BarName, rotation=40)
    
    try :
        plt.savefig('../'+name+'.png')
    except :
        plt.savefig(name+'.png')
#.............................................................................