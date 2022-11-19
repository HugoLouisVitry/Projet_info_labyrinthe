
#111E1111111111111
#10000000001010001
#11111110101011011
#10001000100000001
#11101110101010101
#10000000101010101
#11111111101111101
#10101010000010101
#10101011111010111
#10001010100000101
#11101000111011101
#10001010000000001
#10111011111011101
#10000000001010101
#10101010101010001   
#11111S11111111111
#
#
#
#############################
## ALGORITHME PAR FONCTIONS #
#############################
#
#
#  TRAITEMENT DU FICHIER LABYRINTHE 
## récupère le fichier texte
## lire le fichier 
## Pour chaque carractère on le met dans une liste 
## On crée une matrice qui sera le labyrinthe dont 
## les lignes sont les listes
#
## IDENTIFICATION DES PARRAMETRES 
## identifier les noeuds
#    # on regarde tout les zéros ,
#        # on regarde le nombre de zéro qui entoure ce zéro ,
#            # 1 : cul de sac
#            # 2: c'est juste un chemin
#            # 3 ou 4 : c'est un noeud

## # === INTERFACE GRAPHIQUE === (utiliser tkinter ou turtle)
## mettre des point noirs au mur et blanc aux chemin 
#    # 0:chemin | 1:mur
## symbole début arrivé 
#    # E:2:entrée , S:3:sortie
## visualisation d'un point qui se déplace représentant l'étape de recherche de l'algo
## Ajouter des couleurs

############################
#########   CODE   #########
############################

import tkinter
import numpy as np

# redéfinissez le chemin ( click droit + 'copy path' )
Labyrinthe = "C:\A Mes dossiers\Cours\Supérieur\ENAC\Informatique\Projet Labyrinthe\Labyrinthe.txt"


# === CONVERSION FICHIER EN MATRICE ===
def convert_lab(file):

    lab = open(file, 'r')
    M = []
    for line in lab : 
        L = np.zeros(len(line)-1)
        for (k,char) in enumerate(line) :
            if char.isdecimal() :
                L[k] = int(char)
            else :
                if char == 'E':
                    L[k] = 2
                if char == 'S':
                    L[k] = 3
                if k == len(line)-1:
                    pass            
        M.append(L)
    lab_matrix = np.array(M)

    return lab_matrix


# === IDENTIFICATION DES NOEUDS ET DISTANCES ===


# classe temporaire, on la rempacera par celle du module pour le graphe
class Node:
    def __init__(self,id):
        self.id = id   # coordonnees de la matrice
        self.neightboors_dist = {} # id voisin + distance
        self.how_many_neightboors = len(self.neightboors_dist) # en pratique on lui attribue lors de la recherche des noeuds
        self.entry = False
        self.exit = False

    def define_as_exit(self):
        self.exit = True
        self.entry = False

    def define_as_entry(self):
        self.entry = True
        self.exit = False
    
    def __repr__(self):
        mot = "entree" if self.entry else "sortie" if self.exit else ""
        return f"{str(self.id)}:{str(self.how_many_neightboors)} connections {mot}"

def node_inventory(lab_matrix):
    l,c = lab_matrix.shape

    #contient les noeuds identifiés par coordonnées
    nodes = {}

    def neightboors(i,j):
        #matrice intermédiaire ( forme chelou mais visuelle )
        coord_neightboor = np.array([       [-1,+0],
                                     [+0,-1],       [+0,1],
                                            [+1,+0]   ])
        nb = 0
        for cn in coord_neightboor: # recherche en '+'
            conditions = [i+cn[0] >=0, j+cn[1] >= 0, i+cn[0] < l, j+cn[1] <c]
            if  all(conditions):
                if not lab_matrix[i+cn[0],j+cn[1]] :
                    nb+=1
        return nb

    #recherche des noeuds
    for i in range(l):
        for j in range(c):
            
            
            if lab_matrix[i,j] == 2:            #entree
                nodes[(i,j)] = Node((i,j))
                nodes[(i,j)].define_as_entry()
                nodes[(i,j)].how_many_neightboors=neightboors(i,j)

            if lab_matrix[i,j] == 3:            #sortie
                nodes[(i,j)] = Node((i,j))
                nodes[(i,j)].define_as_exit()
                nodes[(i,j)].how_many_neightboors=neightboors(i,j)
                

            if not lab_matrix[i,j]:
                nb = neightboors(i,j)             #noeud quelquonque
                #nb=0
                #for cn in coord_neightboor: # recherche en '+'
                #    conditions = [i+cn[0] >=0, j+cn[1] >= 0, i+cn[0] < l, j+cn[1] <c]
                #    if  all(conditions):
                #        if not lab_matrix[i+cn[0],j+cn[1]] :
                #            nb+=1
                if nb == 3 or nb == 4:
                    nodes[(i,j)] = Node((i,j))
                    nodes[(i,j)].how_many_neightboors=nb
                    
                
    
    return nodes



if __name__ == '__main__':
    test_lab=convert_lab(Labyrinthe)
    print("\nmatrice labyrinthe \n ",test_lab)
    lab_node = node_inventory(test_lab)
    print("\ndictionnaire des noeuds\n")
    for i in lab_node:
        print(lab_node[i])

