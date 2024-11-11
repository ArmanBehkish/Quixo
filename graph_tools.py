# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:25:33 2022

@author: anton
"""

import numpy as np
import random as rd

"""
Fichier gérant toute requêtes relatives aux graphes.
Deux manières de créer un graphe aléatoire. 
Cf documentation de chaque fonction pour plus de précision.
"""

class graph():
    """
    G              : Matrice d'adjacence du graph'
    n              : Nombre de sommets du graphe  # Doit être supérieur à 4
    m              : Poids maximal de chaque route
    """
    
    Moy_Jour = 0
    Liste_Moyennes_Graphe  = []
    def __init__(self,G = np.array([]), n = 6, m = 809 ,p = None ,t = 96 , Fermeture_Auto = False, Ouverture_Auto = False , Poids_Max = 809 ,Temps_Pause = 1 ):
       
        
        self.n = n
        self.m = m
        self.t = t
      
        self.G = G
        
  

    