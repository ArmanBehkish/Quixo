####  LE PARADOXE DE BRAESS ET SES APPLICATIONS  ####

### Introduction :

#============================================================================#
#----------------------------------------------------------------------------#
#                                   TIPE                                     #
#----------------------------------------------------------------------------#
#                               Antony Davi                                  #
#                      Guillaume Gautier de La Plaine                        #
#                              Roman Rousseau                                #
#                                                                            #
#----------------------------------------------------------------------------#
#                              VERSION 11.0                                  #
#                                                                            #
# o Version la plus aboutie en terme d'exécution pure.                       #
#                                                                            #
# o Toute la simulation ainsi que l'affichage d'une interface Homme/Machine  #
#   fonctionnent correctement.                                               #
#                                                                            #
# o Les valeurs sont pour la plupart choisies de manière aléatoire.          #
#                                                                            #
# o Les seules variables à modifier sont celles dans les deux avant-dernières# 
#   cellules, "Paramètres d'affichage" et "Paramètres de simulation". A voir.#
#                                                                            #
# o Remasterisée sous forme de classe par Antony Davi                        #
#                                                                            #
#----------------------------------------------------------------------------#
#============================================================================#


"""
Par soucis de clarté, les noms des variables (discrètes et globales) sont homogénéisées dans toutes les fonctions.

n                   : Taille du graphe;
Graph.p                   : Proportion de routes inexistantes;
Graph.G                   : Matrice d'adjacence du graphe;
Graph.t                   : Nombre maximal d'itérations;
Graph.Poids_Max           : Poids maximum pour la fermeture automatique si activée;
Graph.Fermeture_Auto      : Active ou non la fermeture automatique;
Graph.Ouverture_Auto      : Active ou non l' ouverture automatique;

City.Liste_Ville*        : Liste des influences des villes, pour une répartition spatiale du traffic;
Rep_Temps*          : Liste de la répartition temporelle du traffic;

Road.Liste_Route*        : Liste des informations sur chaque route;
Epaisseur_Min       : Epaisseur minimale d'une route;
Epaisseur_Max       : Epaisseur maximale d'une route;
(u,v)               : Couple (depart, arrivée) identifiant une route;
Longueur_Min        : Longueur minimale d'une route;
Longueur_Max        : Longueur maximale d'une route;

Block.Liste_Bloc*         : Listge des informations sur chaque bloc de véhicules;
Card_Min            : Cardinal minimum de chaque bloc;
Card_Max            : Cardinal maximum de chaque bloc;
Graph.Matrice_Poids*      : Matrice d'adjacence du graphe, contenant les poids de chaque route;
Graph.Matrice_Cardinal*   : Matrice d'adjacence du graphe, contenant le nombre de personnes sur chaque route;
Graph.Matrice_Etat*       : Matrice d'adjacence du graphe, contenant l'état de chaque route, ouverte ou fermée;
Graph.Matrice_Longueur*   : Matrice d'adjacence du graphe, contenant la longueur de chaque route;

Liste_Moyennes*     : Liste des moyennes des poids sur une simulation.

* : Variables écrasées puis renouvelées à chaque simulation.
"""


### Modules utilisés :

import numpy as np

from tkinter import * 

#Import 

#utils
from utils import *
from graph_tools import graph

#tkinter_tools
from tkinter_tools import *

    
def Afficher(Graph):
    """
    Fonction d'affichage de la matrice des poids ; 1 élément = 1 case
    """
    tailleH=(Rapport-5)//(Graph.n+1)
    tailleV=(Hauteur-5)//(Graph.n+1)
    mat.delete(ALL)
    
    for i in range(Graph.n+1):
        for j in range(Graph.n+1):
            if i==0:
                mat.create_rectangle(j*tailleH, i*tailleV, j*tailleH+tailleH, i*tailleV+tailleV, width=1)
                mat.create_text( (2*j*tailleH+tailleH)/2, (i*tailleV+tailleV)/2, text=str(j-1) , width= tailleH-2)
            if j==0:
                mat.create_rectangle(j*tailleH, i*tailleV, j*tailleH+tailleH, i*tailleV+tailleV, width=1)
                mat.create_text( (2*j*tailleH+tailleH)/2, (2*i*tailleV+tailleV)/2, text=str(i-1) , width= tailleH-2)
            else:
                mat.create_rectangle(j*tailleH, i*tailleV, j*tailleH+tailleH, i*tailleV+tailleV, width=1)

def Iteration():
    """
    Permet d'itérer par le bouton le code principal et d'afficher les listes des routes et des blocs à chaque étape
    """
    pass

def Iteration_Auto():
    
    if Q2=="non" or Q2=="Non":
        return None

def Afficher_Moyennes():
    pass


def Afficher_Courbes():
    pass
def Ouverture_Route_Manuelle():
    pass
    


def Fermeture_Route_Manuelle():
    pass
    



##### Paramètres d'affichage
"""
Ceci est une des deux seules zones à modifier par l'utilisateur, en fonction des paramètres qu'il souhaite.
"""

# Dimensions, pour modifier la taille de l'afficheur.
Longueur = 950
Hauteur = 695
Rapport = (Longueur-300)    # NE PAS MODIFIER


# Autres matrices

GA1 = np.array([[0,1,1,1,0,1],[1,0,1 ,1,1,1],[1,1,0,1,0,0 ],[1,1,1,0,1,1],[0,1,0,1 ,0,0],[1,1,0,1,0,0]])



##### Paramètres de simulation :


x = 0
y = 0


## Script IHM

#Q1 = input("Démarrer ? ")
Q1="oui"
if Q1 == "Oui" or Q1 == "oui" or Q1 == "OUI":
    e = 0  # Indice de l'étape
    d = 1  # Indice de la journée
    Q2 = 1
    print()
    print("Initialisation")
   
    
    #Definition des objets
    Graph = graph(GA1) #Si GA1 n'est pas renseigné , création d'une matrice automatiquement. Les plots ne fonctionneront pas forcément car les routes peuvent ne pas exister.
    print(Graph.G)
    
    n= Graph.n

    
    #Afficheur#
    
    Afficheur = Tk()
    Afficheur.title("Afficheur TIPE")
    Afficheur['bg'] = 'bisque'
    Afficheur.geometry(str(Longueur)+'x'+str(Hauteur)+'+0+0')

    P1 = PanedWindow(Afficheur, handlesize=6, showhandle=False, sashrelief='sunken')
    P1.pack(fill='both')


    # Zonage de l'afficheur
    Matrice = LabelFrame(P1, text="Matrice", borderwidth=2,relief=RAISED, labelanchor="n", width=Rapport, height=Hauteur-5)
    Interface = LabelFrame(P1, text="Interface", borderwidth=2,relief=RAISED, labelanchor="n", width=70, height=Hauteur-5)
    OnOff = LabelFrame(Interface, text="OnOff", borderwidth=2,relief=RAISED, labelanchor="n", width=160, height=200)
    OnOff.pack(side = BOTTOM, padx = 5, pady = 5)


    # Boutons de l'interface
    Quest = Button(Interface, bitmap = 'question', command = Information)
    Quest.pack(side = TOP, padx = 5, pady = 5)
    
    Next = Button(Interface, text = 'Suivant ->', command = Iteration)
    Next.pack(side = TOP, padx = 5, pady = 5)

    Quit = Button(Interface, text = 'Quitter', command = Afficheur.destroy)
    Quit.pack(side = TOP, padx = 5, pady = 5)

    
    Ite_Auto = Button(Interface, text='Journée entière', command = Iteration_Auto)
    Ite_Auto.pack(side = TOP, padx = 5, pady = 5)
    
    AffCourbe = Button(Interface, text = 'Courbes', command = Afficher_Courbes )
   
    AffCourbe.pack(side = TOP,padx = 5,pady = 5)
    
    AffMoyenne = Button(Interface, text = 'Moyennes', command = Afficher_Moyennes )
    
    AffMoyenne.pack(side = TOP,padx = 5,pady = 5)

    # Sous interface de fermeture de route:
    depart= IntVar()
    ChampDep = Entry(OnOff, textvariable= depart, bg ='white', fg='blue')
    ChampDep.pack(side = TOP, padx = 5, pady = 5)
    
    arrivee= IntVar()
    ChampArr = Entry(OnOff, textvariable= arrivee, bg ='white', fg='blue')
    ChampArr.pack(side = TOP, padx = 5, pady = 5)
    
    FR = Button(OnOff, text = 'Fermer!', command = Fermeture_Route_Manuelle)
    FR.pack(side = BOTTOM, padx = 5, pady = 5)

    OU = Button(OnOff, text = 'Ouvrir!', command = Ouverture_Route_Manuelle)
    OU.pack(side = BOTTOM, padx = 5, pady = 5)
    

    # Affichage de la matrice
    mat = Canvas(Matrice, width=Rapport-5, height=Hauteur-10, bg='white')
    mat.pack()
    Afficher(Graph)
    P1.add(Matrice)
    
    #Affichage de l'interface
    P1.add(Interface)
    
    #Affichage l'afficheur
    Afficheur.mainloop()
    