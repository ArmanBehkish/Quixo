# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:24:06 2022

@author: anton
###Petites fonctions utiles

"""
import numpy as np

def maxListe(L):
    m=0
    for i in range(0,len(L)):
        if L[i]>m:
            m=L[i]
    return m

def Morphing_Liste(L):
    """
    Transforme une liste d'éléments en une liste de couples de 2 éléments
    """
    E = []
    
    for i in range(len(L)-1):
        E.append((L[i],L[i+1]))
    return E

### Calcul des moyennes
