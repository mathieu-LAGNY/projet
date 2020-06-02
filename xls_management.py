#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:43:19 2020

@author: mathieu
"""

import xlwt
import xlrd
import itertools

"""Exportation en xls"""

#.............................................................................
#E         result, la liste de tout les résultats
#          name, le nom du fichier à exporter
#Action    Permet d'exporter les résultats sur un graphes en format png
#S         none
def export_xls(result,name):
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Feuille 01')
    
    col_width = 256 * 20
    try:
        for i in itertools.count():
            ws.col(i).width = col_width
    except ValueError:
        pass
    
    st1 = xlwt.easyxf('font: height 200, bold 1; alignment: horizontal center, vertical center; borders: left thin, right thin, top thin, bottom thin') 
    st2 = xlwt.easyxf('font: height 200; alignment: horizontal center, vertical center; borders: left thin, right thin, top thin, bottom thin') 
    
    #En-têtes
    ws.write(0,0,'Masses',st1)
    ws.write(0,1,'Probabilités',st1)
    
    #Valeurs
    for i in range(len(result)):
       ws.write(i+1, 0, result[i][0],st2)
       ws.write(i+1, 1, result[i][1],st2)
    
    try :
        wb.save('../'+name+'.xls')
    except :
        wb.save(name+'.xls')
#.............................................................................

#.............................................................................
#E         none
#Action    Permet l'importation d'un fichier xls pour le calcul inverse
#S         none   
def import_xls():
    
    try :
        
        wb = xlrd.open_workbook('fichier/'+Eimp.get()+'.xls')
        sh = wb.sheet_by_name(wb.sheet_names()[0])
        
        result = []
        result.append(sh.col_values(0)[1:])
        result.append(sh.col_values(1)[1:])
        result.append(sh.col_values(2)[1:])
        
        Lalerti = Label(F3i,text='Le document est en traitement',fg='green',padx=20) 
        Lalerti.grid(row=1,column=1)
        
    except :
        
        Lalerti = Label(F3i,text='Le document est incorrect',fg='red',padx=20) 
        Lalerti.grid(row=1,column=1)
#.............................................................................