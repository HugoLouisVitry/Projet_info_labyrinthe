
import numpy as np
import math as m

import maze_converter
import pimped_heap 
import heapdict as hd



class NotFound (Exception):
    pass


class Node:
    def __init__(self,id):
        self.id = id   # coordonnees de la matrice
        self.neightboors_dist = {} # clé : id voisin , valeur : distance 
        self.how_many_neightboors = len(self.neightboors_dist) # en pratique on lui attribue lors de la recherche des noeuds
        self.entry = False
        self.exit = False
        self.dist= None #distance à la source 
        self.pred = None #precedesseur
        self.closed = False

    def define_as_exit(self):
        self.exit = True
        self.entry = False

    def define_as_entry(self):
        self.entry = True
        self.exit = False
    
    def __repr__(self):
        mot = "entree" if self.entry else "sortie" if self.exit else ""
        return f"{str(self.id)}:{str(self.how_many_neightboors)} connections {mot}"

def traverse (nodes , u ) :
    path = []
    while u is not None :
        path.append ( u )
        u = nodes[u].pred
    path.reverse ()
    return path

#parcours_mono prend en parametre un dictionnaire les clés sont les identifiants des noeuds 
#et les valeurs sont des noeuds de la classe noeud de hugo
def parcours_mono (nodes) : 
    for node in nodes : 
        #print(nodes[node])
        #print(Graphe_Labyrinthe.nodes)
        nodes[node].dist = m.inf
        nodes[node].pred = None
        nodes[node].closed = False
        if nodes[node].entry : 
            id_entree = node
        if nodes[node].exit :
            id_sortie = node
    #print(Graphe_Labyrinthe.nodes)
    nodes[id_entree].dist = 0
    heap =[nodes[id_entree]]

    while heap :
        node = pimped_heap.heappop(heap)
        node.closed = True
        if node.id == id_sortie :
           #print(Graphe_Labyrinthe.traverse( id_sortie ),node.dist)
           return (traverse(nodes , id_sortie ), node.dist )
        for voisin_id in node.neightboors_dist:
            #print(node,voisin_id)
            voisin_dist=node.neightboors_dist[voisin_id]
            if not nodes[voisin_id].closed :
               dist = node.dist + voisin_dist
               v = nodes[ voisin_id ]
               vpred = v.pred
               if v.dist > dist :
                  v.dist = dist
                  v.pred = node.id
               if vpred is None :
                   pimped_heap.heappush( heap , v )
               else :
                    hd.heapdecrease( heap , voisin_id )



if __name__ == '__main__':
    Maze_file= "exemple_labyrinthe.txt"
    Graphic_maze,nodes = maze_converter.get_all(Maze_file)
    #print(nodes)
    maze_converter.graphics(Graphic_maze)
    #print(str(NODE)+"->",nodes[NODE].neightboors_dist,"\n")
    chemin=parcours_mono(nodes)[0]
    maze_converter.update_final(Graphic_maze,chemin)
    maze_converter.graphics(Graphic_maze)
    print(chemin)
