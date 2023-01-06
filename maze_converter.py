############################
#########   CODE   #########
############################

import tkinter
import numpy as np
import operator
import parcoursmono


CHEMIN = 0
MUR = 1
ENTREE = 2
SORTIE = 3
UNDEFINED = 4
VISITED = 5
ACTUAL = 6
PATH = 7


#Labyrinthe = "C:\A Mes dossiers\Cours\Supérieur\ENAC\Informatique\Projet Labyrinthe\Labyrinthe.txt"
#Labyrinthe = "/media/Windows/A Mes dossiers/Cours/Supérieur/ENAC/Informatique/Projet Labyrinthe/Labyrinthe.txt"
Labyrinthe = "/home/hugo/Github/Projet_info_labyrinthe/Labyrinthe.txt"


# === CONVERSION FICHIER EN MATRICE ===
def convert_lab(file):
    """
    Converti un fichier texte en matrice
    """

    lab = open(file, 'r')
    M = []
    for line in lab : 
        L = np.zeros(len(line)-1)
        for (k,char) in enumerate(line) :
            if char.isdecimal() :
                L[k] = int(char)
            else :
                if char == 'E' or char == ENTREE:
                    L[k] = ENTREE
                if char == 'S' or char == SORTIE:
                    L[k] = SORTIE
                if k == len(line)-1:
                    pass            
        M.append(L)
    lab_matrix = np.array(M)

    return lab_matrix

# === IDENTIFICATION DES NOEUDS, DISTANCES ET RELATIONS ===


#matrice des directions de voisinage [ligne,colone,position physique 0 haut, 1 gauche 2 droite,3 bas]
coord_neightboor = np.array([       [-1,+0,0],
                             [+0,-1,1],       [+0,1,2],
                                    [+1,+0,3]   ])

def neightboors(i,j,matrix): 
    """
    Compte le nombre de zéro et leur direction autour d'un 0 (chemin)
    """ 
    l,c = matrix.shape
    nb = 0
    position_0 = [False]*4
    for cn in coord_neightboor: # recherche en '+'
        conditions = [i+cn[0] >=0, j+cn[1] >= 0, i+cn[0] < l, j+cn[1] <c]
        if  all(conditions):
            if not matrix[i+cn[0],j+cn[1]] :
                nb+=1
                position_0[cn[2]] = True
            if matrix[i+cn[0],j+cn[1]] == ENTREE or matrix[i+cn[0],j+cn[1]] == SORTIE:
                nb+=1
                position_0[cn[2]] = True
            
    return nb,position_0

def node_inventory(lab_matrix):
    """
    Identifie et répertorie les noeuds dans le labyrinthe
    """
    l,c = lab_matrix.shape

    #contient les noeuds identifiés par coordonnées
    nodes = {}

    #recherche des noeuds
    turn = {}
    for i in range(l):
        for j in range(c):
            
            nb,position_0 = neightboors(i,j,lab_matrix)

            if lab_matrix[i,j] == ENTREE:            #entree
                nodes[(i,j)] = parcoursmono.Node((i,j))
                nodes[(i,j)].define_as_entry()
                nodes[(i,j)].how_many_neightboors=nb

            if lab_matrix[i,j] == SORTIE:            #sortie
                nodes[(i,j)] = parcoursmono.Node((i,j))
                nodes[(i,j)].define_as_exit()
                nodes[(i,j)].how_many_neightboors=nb


            if not lab_matrix[i,j]:   
                if nb == 1 or nb == 3 or nb == 4:          #noeud quelquonque
                    nodes[(i,j)] = parcoursmono.Node((i,j))
                    nodes[(i,j)].how_many_neightboors=nb
                if nb == 2:
                    if not operator.or_(position_0[0] and position_0[3],position_0[1] and position_0[2]) :
                        turn[(i,j)] = position_0


# ajout des noeuds voisin et de leurs distance (poids)


# count_0 est lancé seulement si cn donne un zéro comme ça on exlcu déjà le cas de rencontre des murs
    def count_0(i,j,direction):
        """
        \nIdentifie le poids d'un voisin : en nombre de zéro case de départ exclue
        \nAlgo récursif
        """
        way = coord_neightboor[direction]
        dist = int(0)
        k = int(1)
        cond =[not lab_matrix[i+way[0]*k,j+way[1]*k],lab_matrix[i+way[0]*k,j+way[1]*k]==3,lab_matrix[i+way[0]*k,j+way[1]*k]==2]
        while any(cond): 
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

    # comptage des poids
    for node in nodes:
        (i,j) = node
        for cn in coord_neightboor: # recherche en '+'
            conditions = [i+cn[0] >=0, j+cn[1] >= 0, i+cn[0] < l, j+cn[1] < c]
            if  all(conditions):
                if not lab_matrix[i+cn[0],j+cn[1]] :
                        c0 = count_0(i,j,cn[2])
                        nodes[(i,j)].neightboors_dist[(c0[1],c0[2])] = c0[0]
                if lab_matrix[i+cn[0],j+cn[1]] == SORTIE or lab_matrix[i+cn[0],j+cn[1]] == ENTREE :
                    c0 = count_0(i,j,cn[2])
                    nodes[(i,j)].neightboors_dist[(c0[1],c0[2])] = c0[0] + 1

    return nodes,turn




# === INTERFACE GRAPHIQUE ===

def graphics(matrix,history=[],path=[]):
    """
    \nInterprétation graphique de la matrice du labyrtinthe
    \nTouche 'q' pour quitter
    \nTouche 'n' pour l'historique
    \nTouche 'a' pour SPLAT 
    
    """
    l,c=matrix.shape
    
    # fenêtre de l'app
    graphic_app = tkinter.Tk()
    graphic_app.title("Recherche dans un labyrinthe")
    
    info = tkinter.Toplevel()
    info.geometry("200x200")
    info_message = tkinter.StringVar()
    info_message.set(f"Distance :  \nNoeud : ( , )")
    info_label = tkinter.Label(info,textvariable=info_message)
    info_label.pack(expand=True)
    history_2 = [data[0] for data in history]

        
    # support du dessin lié à la fenêtre
    SIZE = min(800 // l, 1000 // c)
    map_labyrinthe = tkinter.Canvas(graphic_app,width=c*SIZE,height=l*SIZE,bg='black')
    map_labyrinthe.pack() # met le dessin dans la fenêtre
    map_labyrinthe.focus_set()
    map_labyrinthe.bind('q', lambda _: graphic_app.destroy())
    map_labyrinthe.bind('n', lambda _: story_of_dijkstra(matrix,history,map_labyrinthe,path,info_label,info_message))
    map_labyrinthe.bind('a', lambda _: splat(matrix,history_2,path))

    def splat(matrixed,history_splat,path):
        if len(history_splat):
            for node_id in history_splat:
                (i,j) = node_id
                matrixed[i][j] = VISITED 
        update_final(matrix,path)
        draw(map_labyrinthe,matrixed)

    draw(map_labyrinthe,matrix)
    graphic_app.mainloop()




def draw(canvas=tkinter.Canvas,matrix=np.array):
    """
    \nDessine les cases de la matrices selon leur roles
    """
    l,c = matrix.shape
    SIZE = min(800 // l, 1000// c)
    canvas.delete(tkinter.ALL)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            x1, y1 = j * SIZE, i * SIZE
            x2, y2 = x1 + SIZE, y1 + SIZE
            #labyrinthe
            if not matrix[i][j]:
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')

            #indéfinie ( debugguage generation de labyrinthe)
            if matrix[i][j] == UNDEFINED:
                canvas.create_rectangle(x1, y1, x2, y2, fill='BlueViolet', outline='black')
            #case actuelle
            if matrix[i][j] == ACTUAL :
                canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='white')
            #case visitée
            if matrix[i][j] == VISITED :
                canvas.create_rectangle(x1, y1, x2, y2, fill='green', outline='white')
            #case du chemin
            if matrix[i][j] == PATH :
                canvas.create_rectangle(x1, y1, x2, y2, fill='red', outline='white')
            
            if not i:
                canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='white')
                canvas.create_text((x1+(x2-x1)/2, y1 + (y2-y1)/2), text = f"{j}", fill='white')

            if not j:
                canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='white')
                canvas.create_text((x1+(x2-x1)/2, y1 + (y2-y1)/2), text = f"{i}", fill='white')

            #entrée
            if matrix[i][j] == ENTREE :
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')

                if i == 0 and j != 0:
                    canvas.create_line((x1+x2)/2, y1, (x1+x2)/2, y2, arrow=tkinter.LAST, fill='green', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif i == len(matrix) -1 and j != 0:
                    canvas.create_line((x1+x2)/2, y2, (x1+x2)/2, y1, arrow=tkinter.LAST, fill='green', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif j == 0 and i != 0:
                    canvas.create_line(x1, (y1+y2)/2, x2, (y1+y2)/2, arrow=tkinter.LAST, fill='green', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif j == len(matrix[0])-1 and i != 0:
                    canvas.create_line(x2, (y1+y2)/2, x1, (y1+y2)/2, arrow=tkinter.LAST, fill='green', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                else:
                    canvas.create_oval(x1, y1, x2, y2, fill='green', outline='black')
            #sortie
            if matrix[i][j] == SORTIE :
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
                if i == len(matrix) - 1 and j != 0:
                    canvas.create_line((x1+x2)/2, y1, (x1+x2)/2, y2, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif i == 0 and j!= 0:
                    canvas.create_line((x1+x2)/2, y2, (x1+x2)/2, y1, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif j == len(matrix[0])-1 and i != 0:
                    canvas.create_line(x1, (y1+y2)/2, x2, (y1+y2)/2, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                elif j == 0 and i != 0:
                    canvas.create_line(x2, (y1+y2)/2, x1, (y1+y2)/2, arrow=tkinter.LAST, fill='red', arrowshape= ((y2-y1)/6,(y2-y1)/4,(x2-x1)/4), width=(x2-x1)/5)
                else:
                    canvas.create_oval(x1, y1, x2, y2, fill='red', outline='black')

def story_of_dijkstra(matrix,story,canvas,path,label=tkinter.Label,var=tkinter.StringVar):
    """
    \nRetrace les étapes de la recherche sur l'interface graphique 
    """
    if not len(story):
        print("END or UNDEFINED")
        update_final(matrix,path)
        draw(canvas,matrix)
        var.set(f"\nMeilleur Chemin {path}" )
        
    else :
        (i,j),dist = story.pop(0)
        matrix[i][j] = ACTUAL
        draw(canvas,matrix)
        matrix[i][j] = VISITED
        update_final(matrix,path)
        var.set(f"Distance : {dist} \nNoeud : {(i,j)}")
    
    label.update()

# === Autres ===

def update_final(matrix,path):
    """
    \nImprime sur la matrice le chemin 'path' (uniquement les noeuds)
    \nAppeller ensuite 'graphics' pour l'avoir en couleur
    """
    #print(path)
    if len(path):
        for node_id in path:
            (i,j) = node_id
            matrix[i][j] = PATH 

def get_all(lab_file):
    """
    \nTransforme le fichier texte en matrice et renvoie l'inventaire des noeuds
    """
    Lab_matrix = convert_lab(lab_file)
    Nodes = node_inventory(Lab_matrix)[0]
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
