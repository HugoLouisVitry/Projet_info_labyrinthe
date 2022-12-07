
import numpy as np
import math as m

import Maze_converter
import pimped_heap



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

class WGraph :
    def __init__ ( self ) : 
        self.nodes = {}
    def add_node ( self , u ) :
        self.nodes [ u.id ] = u
    def get_node ( self , u ) :
         return self.nodes [ u ]
    def is_node_in ( self , u ) :
         return u in self.nodes
    def add_edge ( self , u , v , w ) :
        unode = self.nodes.setdefault (u , u )
        if not ( unode.is_adj ( v ) ) : unode.add (v , w )
        vnode = self.nodes.setdefault (v , v )
        if not ( vnode.is_adj ( u ) ) : vnode.add (u , w )
    def remove_edge ( self , u , v ) :
        self.nodes [ u ].remove ( v )
        self.nodes [ v ].remove ( u )
    def weight ( self , u , v ) :
        return self.nodes [ u ]. weight ( v )
    def neighbour ( self , u ) :
            return self.nodes [ u ].neighbours () 

    def traverse (self , u ) :
        path = []
        while u is not None :
            path.append ( u )
            u = self.nodes[u].pred
        path.reverse ()
        return path

#parcours_mono prend en parametre un dictionnaire les clés sont les identifiants des noeuds 
#et les valeurs sont des noeuds de la classe noeud de hugo
def parcours_mono (nodes , id_entree , id_sortie ) : 
    Graphe_Labyrinthe = WGraph () 
    for node in nodes : 
        #print(nodes[node])
        Graphe_Labyrinthe.add_node(nodes[node])
        #print(Graphe_Labyrinthe.nodes)
        nodes[node].dist = m.inf
        nodes[node].pred = None
        nodes[node].closed = False
    #print(Graphe_Labyrinthe.nodes)
    Graphe_Labyrinthe.nodes[id_entree].dist = 0
    heap =[ Graphe_Labyrinthe.nodes[id_entree]]

    while heap :
        node = pimped_heap.heappop(heap)
        node.closed = True
        if node.id == id_sortie :
           #print(Graphe_Labyrinthe.traverse( id_sortie ),node.dist)
           return (Graphe_Labyrinthe.traverse( id_sortie ), node.dist )
        for voisin_id in node.neightboors_dist:
            #print(node,voisin_id)
            voisin_dist=node.neightboors_dist[voisin_id]
            if not Graphe_Labyrinthe.nodes[voisin_id].closed :
               dist = node.dist + voisin_dist
               v = Graphe_Labyrinthe.nodes[ voisin_id ]
               vpred = v.pred
               if v.dist > dist :
                  v.dist = dist
                  v.pred = node.id
               if vpred is None :
                   pimped_heap.heappush( heap , v )
#               else :
#                    hq.heapdecrease( heap , voisin_id )



if __name__ == '__main__':
    Maze_file= "lab.txt"
    Graphic_maze,nodes = Maze_converter.get_all(Maze_file)
    #print(nodes)
    Maze_converter.graphics(Graphic_maze)

    for NODE in nodes:
        #print(str(NODE)+"->",nodes[NODE].neightboors_dist,"\n")
        if nodes[NODE].entry:
            id_entree = nodes[NODE].id
        if nodes[NODE].exit:
            id_sortie = nodes[NODE].id
    chemin=parcours_mono(nodes,id_entree,id_sortie)[0]
    Maze_converter.update_final(Graphic_maze,chemin)
    Maze_converter.graphics(Graphic_maze)

    
