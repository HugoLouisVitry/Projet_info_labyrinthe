
#imports

import tkinter
import numpy as np
import operator
import node_master

# variables globales
FACTOR = 1
CHEMIN = 0
MUR = 1
ENTREE = 2
SORTIE = 3
BACK_PATH = 4
VISITED = 5
ACTUAL = 6
PATH = 7
OFFSET_i = 0
OFFSET_j = 0
HAUTEUR = 1000
LARGEUR = 1000
Labyrinthe_test = "/home/hugo/Documents/Enac/Projet info programmes Oral/Labyrinthe.txt"

graph_regulier = np.zeros((100,100))
L,C=graph_regulier.shape
for i in range(0,L-1,2):
    for j in range(0,C-1,2):
        graph_regulier[i][j]=1
graph_regulier[10][10]=2
graph_regulier[45][45]=3

# === CONVERSION FICHIER EN MATRICE ===

def convert_lab(file):
    """
    Converti un fichier texte en matrice
    Donner le chemin d'accès au fichier
    """

    M = []
    with open(file, 'r') as lab:
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
    Pour obtenir les noeud récupérer le 1er élément du tuple de sortie
    """
    l,c = lab_matrix.shape
    nodes = {} #contient les noeuds identifiés par coordonnées
    turn = {} # contient les virages

    #recherche des noeuds
    for i in range(l):
        for j in range(c):
            
            nb,position_0 = neightboors(i,j,lab_matrix)

            if lab_matrix[i,j] == ENTREE:            #entree
                nodes[(i,j)] = node_master.Node((i,j))
                nodes[(i,j)].define_as_entry()
                nodes[(i,j)].how_many_neightboors=nb

            if lab_matrix[i,j] == SORTIE:            #sortie
                nodes[(i,j)] = node_master.Node((i,j))
                nodes[(i,j)].define_as_exit()
                nodes[(i,j)].how_many_neightboors=nb


            if not lab_matrix[i,j]:   
                if nb == 1 or nb == 3 or nb == 4:          #noeud quelquonque
                    nodes[(i,j)] = node_master.Node((i,j))
                    nodes[(i,j)].how_many_neightboors=nb
                if nb == 2:  # virages
                    # on vérifie qu'on change bien de direction, sinon c'est un couloir
                    if not operator.or_(position_0[0] and position_0[3],position_0[1] and position_0[2]) :
                        turn[(i,j)] = position_0

# ajout des noeuds voisin et de leurs distance (poids)

    # count_0 est lancé seulement si cn(défini après) donne une case chemin comme ça on exlcu déjà le cas de rencontre des murs
    def count_0(i,j,direction):
        """
        \nIdentifie le poids d'un voisin : en nombre de zéro case de départ exclue
        \nAlgo récursif
        """
        way = coord_neightboor[direction]
        dist = int(0)
        k = int(1)
        condition =[not lab_matrix[i+way[0]*k,j+way[1]*k],lab_matrix[i+way[0]*k,j+way[1]*k]==3,lab_matrix[i+way[0]*k,j+way[1]*k]==2]
        while any(condition):
            dist+=1
            
            if (i+way[0]*k,j+way[1]*k) in nodes : # si la case est un noeud on ajoute le voisin et le poids
                return dist ,i+way[0]*k,j+way[1]*k
                
            elif (i+way[0]*k,j+way[1]*k) in turn : # si la case est un virage on relance la recherche(récursivement) en changeant la direction
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
            else : # si aucun cas on continue en changeant de case et on incrémnte la distance
                k+=1

        return (0,0,0)
    #fin count_0

    # comptage des poids
    for node in nodes:
        (i,j) = node
        for cn in coord_neightboor: # recherche en '+'
            conditions = [i+cn[0] >=0, j+cn[1] >= 0, i+cn[0] < l, j+cn[1] < c]
            if  all(conditions): # ainsi on ne lance count_0 qu'hors des murs
                if not lab_matrix[i+cn[0],j+cn[1]] : 
                        c0 = count_0(i,j,cn[2])
                        nodes[(i,j)].neightboors_dist[(c0[1],c0[2])] = c0[0]
                if lab_matrix[i+cn[0],j+cn[1]] == SORTIE or lab_matrix[i+cn[0],j+cn[1]] == ENTREE :
                    c0 = count_0(i,j,cn[2])
                    nodes[(i,j)].neightboors_dist[(c0[1],c0[2])] = c0[0] + 1
    return nodes,turn




# === INTERFACE GRAPHIQUE ===

def graphics(matrix,history=[],path=[],reset=0,history_reverse=[]):
    """
    \nInterprétation graphique de la matrice du labyrtinthe
    \nTouche 'q' quitter
    \nTouche 'n' historique
    \nTouche 'a' surface totale 
    \nTouche 'z' zoom +  
    \nTouche 'e' zoom - 
    \nTouche 'b' reset zoom 
    """
    l,c=matrix.shape
    
    # fenêtre de l'app
    graphic_app = tkinter.Tk()
    graphic_app.title("Recherche dans un labyrinthe")
    
    # fenêtre de suivit
    info = tkinter.Toplevel()
    info.geometry("200x200")
    info_message = tkinter.StringVar()
    info_message.set(f"Taille{l}x{c}\nDistance :  \nNoeud : ( , )")
    info_label = tkinter.Label(info,textvariable=info_message)
    info_label.pack(expand=True)
    history_ = [data[0] for data in history]
    history_rev_ = [data[0] for data in history_reverse]    

    # fonction de zoom (fonctionne partiellement) il faudrait une fonction de scrolling avec
    def refactor(o):
        global FACTOR
        if not o :
            FACTOR = 1
        else :
            FACTOR *= o
        draw(map_labyrinthe,matrix)

    # fonction de déplacement de l'image
    def change_offset(N):
        global OFFSET_i
        global OFFSET_j
        if N == 1:#haut
            OFFSET_i = OFFSET_i+int(10) if OFFSET_i+int(10) <= l-1 else l-1
        if N == 2:#bas
            OFFSET_i = OFFSET_i-int(10) if OFFSET_i-int(10) >= 0  else 0
        if N == 3:#droite
            OFFSET_j = OFFSET_j+int(10) if OFFSET_j+int(10) <= c-1 else c-1
        if N == 4:#gauche
            OFFSET_j = OFFSET_j-int(10) if OFFSET_j-int(10) >= 0  else 0
        if not N:
            OFFSET_i = 0
            OFFSET_j = 0
        draw(map_labyrinthe,matrix)


    # support du dessin lié à la fenêtre
    SIZE = min(HAUTEUR // l, LARGEUR // c) * FACTOR
    map_labyrinthe = tkinter.Canvas(graphic_app,width=c*SIZE,height=l*SIZE,bg='grey')
    map_labyrinthe.pack(expand=True) # met le dessin dans la fenêtre
    map_labyrinthe.focus_set()
    map_labyrinthe.bind('q', lambda _: graphic_app.destroy())
    map_labyrinthe.bind('n', lambda _: story_of_dijkstra(matrix,history,map_labyrinthe,path,info_label,info_message))
    map_labyrinthe.bind('a', lambda _: splat(matrix,history_,path,reset,history_rev_))
    map_labyrinthe.bind('z', lambda _: refactor(2))
    map_labyrinthe.bind('e', lambda _: refactor(0.5))
    map_labyrinthe.bind('g', lambda _: change_offset(1))#haut
    map_labyrinthe.bind('t', lambda _: change_offset(2))#bas
    map_labyrinthe.bind('h', lambda _: change_offset(3))#droite
    map_labyrinthe.bind('f', lambda _: change_offset(4))#gauche
    map_labyrinthe.bind('r', lambda _: refactor(0),change_offset(0))#reset

    


    def splat(Matrix,history_splat,path,reset=0,History_reverse=[]):
        """
        Affiche l'ensemble de la surface balayée par node_master
        """
        color = CHEMIN if reset else VISITED
        if len(history_splat):
            for (i,j) in history_splat:
                Matrix[i][j] =  color

        if len(History_reverse): # couleur différente pour le double node_master 
            for (i,j) in History_reverse:
                Matrix[i][j] =  BACK_PATH # a grande echelle on ne distingue que noir et blanc, sur fond noir -> ce n'est pas fonctionnel
    
        update_final(matrix,path)
        draw(map_labyrinthe,Matrix)

    draw(map_labyrinthe,matrix)
    graphic_app.mainloop()




def draw(canvas=tkinter.Canvas,matrix=np.array):
    """
    \nDessine les cases de la matrices selon leur roles
    """
    l,c = matrix.shape
    SIZE = min(HAUTEUR // l, LARGEUR// c)*FACTOR
    canvas.delete(tkinter.ALL)
    for i in range(OFFSET_i,len(matrix)):
        for j in range(OFFSET_j,len(matrix[0])):
            x1, y1 = (j-OFFSET_j) * SIZE, (i-OFFSET_i) * SIZE
            x2, y2 = x1 + SIZE, y1 + SIZE
            #labyrinthe
            if matrix[i][j] == MUR:
                canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='black')
            
            if not matrix[i][j]:
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')

            #retour double node_master
            if matrix[i][j] == BACK_PATH:
                canvas.create_rectangle(x1, y1, x2, y2, fill='BlueViolet', outline='BlueViolet')
            #case actuelle
            if matrix[i][j] == ACTUAL :
                canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='white')
                canvas.create_text((x1+(x2-x1)/2, y1 + (y2-y1)/2), text = f"({i},{j})", fill='white')

            #case visitée
            if matrix[i][j] == VISITED :
                canvas.create_rectangle(x1, y1, x2, y2, fill='cyan', outline='cyan')
            #case du chemin
            if matrix[i][j] == PATH :
                canvas.create_rectangle(x1, y1, x2, y2, fill='red', outline='red')
            
            # numéros des cases
            if not i-OFFSET_i:

                canvas.create_text((x1+(x2-x1)/2, y1 + (y2-y1)/2), text = f"{j}", fill='magenta')

            if not j-OFFSET_j:

                canvas.create_text((x1+(x2-x1)/2, y1 + (y2-y1)/2), text = f"{i}", fill='magenta')

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
    \nATTENTION NE PAS SPAMMER LA TOUCHE 'n' : Risque d'overflow
    """
    l,c = matrix.shape
    if not len(story):
        print("END or UNDEFINED")
        update_final(matrix,path)
        draw(canvas,matrix)
        var.set(f"Taille{l}x{c}\nMeilleur Chemin {path}" )
        
    else :
        (i,j),dist = story.pop(0)
        matrix[i][j] = ACTUAL
        draw(canvas,matrix)
        matrix[i][j] = VISITED
        update_final(matrix,path)
        var.set(f"Taille{l}x{c}\nDistance : {dist} \nNoeud : {(i,j)}")
    
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

    # Démo examen 

    test_lab=convert_lab(Labyrinthe_test)
    print("\nmatrice labyrinthe \n",test_lab)
    lab_node,turns = node_inventory(test_lab)
    print("\ndictionnaire des noeuds\n")
    for i in lab_node:
        print(lab_node[i],"\t|",lab_node[i].neightboors_dist)
    print("\nvirages\n")
    for i in turns:
        print(i)
    graphics(test_lab)

    
