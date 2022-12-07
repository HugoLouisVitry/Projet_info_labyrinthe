
import numpy as np
import math as m
import heapq as hq

import Maze_converter

def heappop_modified(heap):
    """Pop the smallest item off the heap, maintaining the heap invariant."""
    lastelt = heap.pop()    # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        _siftup_modified(heap, 0)
        return returnitem
    return lastelt
def _siftup_modified(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2*pos + 1    # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos].dist < heap[rightpos].dist:
            childpos = rightpos
        # Move the smaller child up.
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    _siftdown_modified(heap, startpos, pos)   

def heappush_modified(heap, item):
    """Push item onto heap, maintaining the heap invariant."""
    heap.append(item)
    _siftdown_modified(heap, 0, len(heap)-1)

def _siftdown_modified(heap, startpos, pos):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem.dist < parent.dist:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem


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
         node = heappop_modified(heap)
         node.closed = True
         if node.id == id_sortie :
            print(Graphe_Labyrinthe.traverse( id_sortie ),node.dist)
            return ( node.dist , Graphe_Labyrinthe.traverse( id_sortie ) )
         for voisin_id in node.neightboors_dist:
             print(node,voisin_id)
             voisin_dist=node.neightboors_dist[voisin_id]
             if not Graphe_Labyrinthe.nodes[voisin_id].closed :
                dist = node.dist + voisin_dist
                v = Graphe_Labyrinthe.nodes[ voisin_id ]
                vpred = v.pred

                if v.dist > dist :
                   v.dist = dist
                   v.pred = node.id
                if vpred is None :
                    heappush_modified ( heap , v )
#                else :
#                    hq.heapdecrease( heap , voisin_id )



if __name__ == '__main__':
    Maze_file= "lab.txt"
    Graphic_maze,nodes = Maze_converter.get_all(Maze_file)
    print(nodes)
    Maze_converter.graphics(Graphic_maze)

    for NODE in nodes:
        print(nodes[NODE].neightboors_dist)
        if nodes[NODE].entry:
            id_entree = nodes[NODE].id
        if nodes[NODE].exit:
            id_sortie = nodes[NODE].id
    parcours_mono(nodes,id_entree,id_sortie)
