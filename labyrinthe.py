
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
## état des cases
#    #4:case actuelle,
#    #5:case visité,
#    #6:cul de sac,
#    #7:meilleur chemin
#
## visualisation d'un point qui se déplace représentant 
#  l'étape de recherche de l'algo, en temps réel ou sous 
#  forme d'animation après calcul
#       # IL s'agit d'un objet qui contient les attribut suivants
        # dans un premier temps
            # sa position dans la matrice 
            # liste de toutes les cases visitées
        # dans un deuxième temps
            # connaissance des chemins 
            # à determiner
# il s'agit de mettre à jour la matrice à chaque étape en 
# modifiant une case vide en case état ou visité 
# voir marquer les chemins menant a des culs de sacs
## Ajouter des couleurs

############################
#########   CODE   #########
############################

import tkinter
import numpy as np
import operator
# redéfinissez le chemin ( click droit + 'copy path' )

Labyrinthe = "C:\A Mes dossiers\Cours\Supérieur\ENAC\Informatique\Projet Labyrinthe\Labyrinthe.txt"
#Labyrinthe = "/media/Windows/A Mes dossiers/Cours/Supérieur/ENAC/Informatique/Projet Labyrinthe/Labyrinthe.txt"






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







# === IDENTIFICATION DES NOEUDS, DISTANCES ET RELATIONS ===


# classe temporaire, on la rempacera par celle du module pour le graphe
class GraphModuleNode:
    def __init__(self,id):
        self.id = id   # coordonnees de la matrice, mettez un tuple
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


#matrice des directions de voisinage [ligne,colone,position physique 0 haut, 1 gauche 2 droite,3 bas]
coord_neightboor = np.array([       [-1,+0,0],
                             [+0,-1,1],       [+0,1,2],
                                    [+1,+0,3]   ])

def neightboors(i,j,matrix): # compte le nombre de zéro et leur direction autour d'un 0 
    l,c = matrix.shape
    nb = 0
    position_0 = [False]*4
    for cn in coord_neightboor: # recherche en '+'
        conditions = [i+cn[0] >=0, j+cn[1] >= 0, i+cn[0] < l, j+cn[1] <c]
        if  all(conditions):
            if not matrix[i+cn[0],j+cn[1]] :
                nb+=1
                position_0[cn[2]] = True
            if matrix[i+cn[0],j+cn[1]] == 2 or matrix[i+cn[0],j+cn[1]] == 3:
                nb+=1
                position_0[cn[2]] = True
            
    return nb,position_0

def node_inventory(lab_matrix):
    l,c = lab_matrix.shape

    #contient les noeuds identifiés par coordonnées
    nodes = {}

    #recherche des noeuds
    turn = {}
    for i in range(l):
        for j in range(c):
            
            nb,position_0 = neightboors(i,j,lab_matrix)

            if lab_matrix[i,j] == 2:            #entree
                nodes[(i,j)] = GraphModuleNode((i,j))
                nodes[(i,j)].define_as_entry()
                nodes[(i,j)].how_many_neightboors=nb

            if lab_matrix[i,j] == 3:            #sortie
                nodes[(i,j)] = GraphModuleNode((i,j))
                nodes[(i,j)].define_as_exit()
                nodes[(i,j)].how_many_neightboors=nb


            if not lab_matrix[i,j]:   
                if nb == 1 or nb == 3 or nb == 4:          #noeud quelquonque
                    nodes[(i,j)] = GraphModuleNode((i,j))
                    nodes[(i,j)].how_many_neightboors=nb
                if nb == 2:
                    if not operator.or_(position_0[0] and position_0[3],position_0[1] and position_0[2]) :
                        turn[(i,j)] = position_0


# ajout des noeuds voisin et de leurs distance (poids)
#
# count_0 est lancé seulement si cn donne un zéro comme ça on exlcu déjà le cas de rencontre des murs
    def count_0(i,j,direction): # récursif
        way = coord_neightboor[direction]
        dist = int(0)
        k = int(1)
        
        while not lab_matrix[i+way[0]*k,j+way[1]*k]: 
            dist+=1
            if (i+way[0]*k,j+way[1]*k) in nodes :
                return dist ,i+way[0]*k,j+way[1]*k
                
            elif (i+way[0]*k,j+way[1]*k) in turn :
                change_to_direction = None
                if way[2] in (0,3) : # vertical
                    gauche = turn[(i+way[0]*k,j+way[1]*k)][1]
                    # 2 vers la droite // droite = turn[(i+cn[0]*k,j+cn[1]*k)][2]
                    change_to_direction = 1 if gauche else 2   
                elif way[2] in (1,2) : # horizontal
                    haut = turn[(i+way[0]*k,j+way[1]*k)][0]
                    # 3 vers le bas // bas = turn[(i+cn[0]*k,j+cn[1]*k)][3]
                    change_to_direction = 0 if haut else 3   
                            
                c=count_0(i+way[0]*k,j+way[1]*k,change_to_direction)
                return c[0]+dist,c[1],c[2]
            else : 
                k+=1
        return (0,0,0) # jamais utilisé mais j'ai des problèmes d'interpretation si je le met pas

    #fin count_0

#    # comptage des poids
#    for node in nodes:
#        (i,j) = node
#        for cn in coord_neightboor: # recherche en '+'
#            conditions = [i+cn[0] >=0, j+cn[1] >= 0, i+cn[0] < l, j+cn[1] <c]
#            print(conditions)
#            if  all(conditions):
#                if not lab_matrix[i+cn[0],j+cn[1]] :
#                        c = count_0(i,j,cn[2])
#                        nodes[(i,j)].neightboors_dist[(c[1],c[2])] = c[0]

    return nodes,turn




# === INTERFACE GRAPHIQUE ===

def graphics(matrix):
    l,c=matrix.shape
    
    # fenêtre de l'app
    graphic_app = tkinter.Tk()
    graphic_app.title("Recherche dans un labyrinthe")

    # support du dessin lié à la fenêtre
    SIZE = min(800 // l, 1000 // c)
    map_labyrinthe = tkinter.Canvas(graphic_app,width=c*SIZE,height=l*SIZE,bg='black')
    map_labyrinthe.pack() # met le dessin dans la fenêtre
    map_labyrinthe.focus_set()
    map_labyrinthe.bind('q', lambda _: graphic_app.destroy())
    draw(map_labyrinthe,matrix)
    graphic_app.mainloop()

def draw(canvas,matrix):
    l,c = matrix.shape
    SIZE = min(800 // l, 1000// c)
    canvas.delete(tkinter.ALL)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            
            #labyrinthe
            if not matrix[i][j]:
                x1, y1 = j * SIZE, i * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
            #entrée
            if matrix[i][j] == 2 :
                x1, y1 = j * SIZE, i * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')

                if i == 0 and j != 0:
                    canvas.create_line((x1+x2)/2, y1, (x1+x2)/2, y2, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif i == len(matrix) -1 and j != 0:
                    canvas.create_line((x1+x2)/2, y2, (x1+x2)/2, y1, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif j == 0 and i != 0:
                    canvas.create_line(x1, (y1+y2)/2, x2, (y1+y2)/2, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif j == len(matrix[0])-1 and i != 0:
                    canvas.create_line(x2, (y1+y2)/2, x1, (y1+y2)/2, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
            #sortie
            if matrix[i][j] == 3 :
                x1, y1 = j * SIZE, i * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
                if i == len(matrix) - 1 and j != 0:
                    canvas.create_line((x1+x2)/2, y1, (x1+x2)/2, y2, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif i == 0 and j!= 0:
                    canvas.create_line((x1+x2)/2, y2, (x1+x2)/2, y1, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif j == len(matrix[0])-1 and i != 0:
                    canvas.create_line(x1, (y1+y2)/2, x2, (y1+y2)/2, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif j == 0 and i != 0:
                    canvas.create_line(x2, (y1+y2)/2, x1, (y1+y2)/2, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)

            #case actuelle
            if matrix[i][j] == 4 :
                x1, y1 = j * SIZE, i * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='white')
            #case visitée
            if matrix[i][j] == 5 :
                x1, y1 = j * SIZE, i * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill='cyan', outline='white')


## il s'agit d'un objet qui fera référence 
## à l'état d'avancement de l'algorithme de recherche 
## il est la pour faire des test
#state = [(2,1),[]]
#
##met à jour les cases de la matrice numérique
#def maj(state,matrix):
#    matrix[state[0]] = 4
##    for i in state[1]:
##        matrix[i]






def get_all(lab_file):
    Lab_matrix = convert_lab(lab_file)
    Nodes = node_inventory(Lab_matrix)
    return Lab_matrix,Nodes

if __name__ == '__main__':
    test_lab=convert_lab(Labyrinthe)
    print("\nmatrice labyrinthe \n",test_lab)
    lab_node,turns = node_inventory(test_lab)
    print("\ndictionnaire des noeuds\n")
    for i in lab_node:
        print(lab_node[i],"|",lab_node[i].neightboors_dist)
    print("\n virages \n")
    for i in turns:
        print(i)
    graphics(test_lab)


    
