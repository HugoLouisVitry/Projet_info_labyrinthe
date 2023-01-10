
import math as m
import maze_converter
import pimped_heap
import time



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
        self.reverse_closed = False
        self.reverse_pred = None
        self.reverse_dist = None

    def define_as_exit(self):
        self.exit = True
        self.entry = False

    def define_as_entry(self):
        self.entry = True
        self.exit = False
    
    def __repr__(self):
        mot = "entree" if self.entry else "sortie" if self.exit else ""
        return f"{str(self.id)}:"#{str(self.how_many_neightboors)} connections {mot}"


def traverse (nodes , u ,reverse = False) :
    path = []
    if reverse :
        while u is not None :
            path.append ( u )
            u = nodes[u].reverse_pred
    else :
        while u is not None :
            path.append ( u )
            u = nodes[u].pred
        path.reverse ()

    return path
    
#parcours_mono prend en parametre un dictionnaire les clés sont les identifiants des noeuds 
#et les valeurs sont des noeuds de la classe noeud de hugo
def dijkstra_mono (nodes) : 

    for node in nodes : 
        nodes[node].dist = m.inf
        nodes[node].pred = None
        nodes[node].closed = False
        if nodes[node].entry : 
            id_entree = node
        if nodes[node].exit :
            id_sortie = node

    nodes[id_entree].dist = 0
    heap =[nodes[id_entree]]
    history=[]

    t0=time.time()
    while heap :
        #print("\n while heap: ",heap)
        history.append((heap[0].id,heap[0].dist))
        node = pimped_heap.heappop(heap)
        node.closed = True
        if node.id == id_sortie :
            T = time.time()-t0
            print("\n\nTERMINATED MONO")
            return (traverse(nodes , id_sortie ), node.dist ,history,T)
        for voisin_id in node.neightboors_dist:
            #print("heap: ",heap)
            #print("actual: ",node,voisin_id)
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
                    #print("push: ",v)
                 
                else :
                    #print("decrease: ",v)
                    pimped_heap.decrease_key(heap , v )
                
def dijkstra_double (nodes) : 

    for node in nodes : 
        nodes[node].dist = m.inf
        nodes[node].reverse_dist = m.inf
        nodes[node].pred = None
        nodes[node].reverse_pred = None
        nodes[node].closed = False
        nodes[node].reverse_closed = False
        
        if nodes[node].entry : 
            id_entree = node
        if nodes[node].exit :
            id_sortie = node

    nodes[id_entree].dist = 0
    nodes[id_sortie].reverse_dist = 0
    heap = [nodes[id_entree]]
    heap_reverse = [nodes[id_sortie]]
    history=[]
    history_reverse=[]
    history_total = []

    prec_heap_node = None
    reverse = False
#    i = 0
#    print("base")
#    print(heap)
#    print(heap_reverse)
#    print("begin loop")
    t0=time.time()

    while heap or heap_reverse:
        #i+=1
        #print(i)
    
        # conserve le rayon de recherche le plus court
            
        if heap and heap_reverse:
            if heap[0].dist <= heap_reverse[0].reverse_dist :
                if heap[0] == prec_heap_node:
                    history_reverse.append((heap_reverse[0].id,heap_reverse[0].reverse_dist))
                    node = pimped_heap.heappop(heap_reverse)
                    reverse = True
                  #  print("heap_reverse")
                else :
                    history.append((heap[0].id,heap[0].dist))
                    node = pimped_heap.heappop(heap)
                    reverse = False
                 #   print("heap")
            else:
                history_reverse.append((heap_reverse[0].id,heap_reverse[0].reverse_dist))
                node = pimped_heap.heappop(heap_reverse)
                reverse = True
           #     print("heap_reverse")

        elif heap :
            history.append((heap[0].id,heap[0].dist))
            node = pimped_heap.heappop(heap)
            reverse = False
           # print("heap only")
        
        elif heap_reverse : 
            history_reverse.append((heap_reverse[0].id,heap_reverse[0].reverse_dist))
            node = pimped_heap.heappop(heap_reverse)
            reverse = True
            #print("heap_reverse only")

        #print("prec node ",prec_heap_node)        
        #print("actual ",node)
        # nouvelle condition, si le noeud est déjà fermé lors du passage de la recherche dans un sens 
        # c'est que la recherche dans l'autre sens l'a déjà trouvé, et donc jointure !
        history_total.append((node.id,node.dist))
        if node.closed or node.reverse_closed:
            T=time.time()-t0
            print("\n\nTERMINATED DOUBLE")
            
            path = traverse(nodes,node.pred) + [node.id] + traverse(nodes,node.reverse_pred,True)

            print("sense 1 ", traverse(nodes,node.id),"\nsens2 ",traverse(nodes,node.reverse_pred,True))
            return (path, node.dist ,history,history_reverse,history_total,T)

        else :
            if reverse :
                node.reverse_closed = True
            else:
                node.closed = True
            prec_heap_node = node
            #print(node.id," closed ")

        for voisin_id in node.neightboors_dist:

            voisin_dist=node.neightboors_dist[voisin_id]

            if reverse:
                if not nodes[voisin_id].reverse_closed :
                    dist = node.reverse_dist + voisin_dist
                    v = nodes[ voisin_id ]
                    vpred = v.reverse_pred
                    if v.reverse_dist > dist :
                        v.reverse_dist = dist
                        v.reverse_pred = node.id
                        if vpred is None :
                            pimped_heap.heappush(heap_reverse, v, reverse)
                        else :
                            pimped_heap.decrease_key(heap_reverse, v, reverse)

            else :
                if not nodes[voisin_id].closed :
                   dist = node.dist + voisin_dist
                   v = nodes[ voisin_id ]
                   vpred = v.pred
                   if v.dist > dist :
                        v.dist = dist
                        v.pred = node.id
                        if vpred is None :
                            pimped_heap.heappush(heap, v)
                        else :
                            pimped_heap.decrease_key(heap, v)



if __name__ == '__main__':
    Maze_file= "/home/hugo/Github/Projet_info_labyrinthe/Labyrinthe.txt"
    Graphic_maze,nodes = maze_converter.get_all(Maze_file)
    #print(nodes)
    maze_converter.graphics(Graphic_maze)

    #for NODE in nodes:
    #    #print(str(NODE)+"->",nodes[NODE].neightboors_dist,"\n")
    #    if nodes[NODE].entry:
    #        id_entree = nodes[NODE].id
    #    if nodes[NODE].exit:
    #        id_sortie = nodes[NODE].id
    #chemin,distance,history=dijkstra_mono(nodes)
    

    chemin,distance,history=dijkstra_mono(nodes)
    print("Distance : ",distance,"\nChemin :",chemin)
    
    maze_converter.update_final(Graphic_maze,chemin)
    maze_converter.graphics(Graphic_maze,history,chemin)
    
    maze_converter.graphics(Graphic_maze,reset=1)
    
    Chemin2, Distance2,history2,history2_reverse,h_total,T = dijkstra_double(nodes)
    print("Distance : ",Distance2,"\nChemin :",Chemin2)
    maze_converter.graphics(Graphic_maze,h_total,Chemin2,history_reverse=history2_reverse)

    

   
