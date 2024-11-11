# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:50:27 2022

@author: anton
"""

### Fonctions utilisées dans le script d'affichage

# Fonctions avec fonctionnement indépendant du script :
from tkinter import messagebox


# Fonctions dont le fonctionnement est lié au script :

def Information():
    """
    Message d'information de l'afficheur.
    """
    Aide = "This interface is used to simulate traffic on a road network, in order to verify the Braess Paradox. \n \n Version 11.0 . The program dates from 16/02/2019 and was remasterised in october 2022 \n \n Made by Guillaume Gautier de La Plaine, Roman Rousseau and Antony Davi."
    
    messagebox.showinfo("Aide Afficheur", Aide)