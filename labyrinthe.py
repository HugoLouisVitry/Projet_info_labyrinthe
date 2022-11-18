"""
111E1111111111111
10000000001010001
11111110101011011
10001000100000001
11101110101010101
10000000101010101
11111111101111101
10101010000010101
10101011111010111
10001010100000101
11101000111011101
10001010000000001
10111011111011101
10000000001010101
10101010101010001   
11111S11111111111

"""

############################
# ALGORITHME PAR FONCTIONS #
############################


# ||| TRAITEMENT DU FICHIER LABYRINTHE |||
# récupère le fichier texte
# lire le fichier 
# Pour chaque carractère on le met dans une liste 
# On crée une matrice qui sera le labyrinthe dont 
# les lignes sont les listes

# ||| IDENTIFICATION DES PARRAMETRES |||
# identifier les noeuds
    # on regarde tout les zéros ,
        # on regarde le nombre de zéro qui entoure ce zéro ,
            # 1 : cul de sac
            # 2: c'est juste un chemin
            # 3 ou 4 : c'est un noeud


# # ||| INTERFACE GRAPHIQUE ||| (utiliser tkinter ou turtle)
# mettre des point noirs au mur et blanc aux chemin 
    # 0:chemin | 1:mur
# symbole début arrivé 
    # E:2:entrée , S:3:sortie
# visualisation d'un point qui se déplace représentant l'étape de recherche de l'algo
# Ajouter des couleurs

############################
#########   CODE   #########
############################

import tkinter
import numpy as np

# redéfinissez le chemin ( click droit + 'copy path' )
Labyrinthe = "C:\A Mes dossiers\Cours\Supérieur\ENAC\Informatique\Projet Labyrinthe\Labyrinthe.txt"

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

if __name__ == '__main__':
    print(convert_lab(Labyrinthe))


