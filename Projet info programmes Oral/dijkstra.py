
import math as m
import maze_converter
import pimped_heap
import time
import operator


class NotFound (Exception):
    pass

def traverse (nodes , u ,reverse = False) :
    """
    \nRetrace l'ensembles des parents pour récupérer le chemin
    """
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

def definition_entree_sortie (nodes) :
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
        return id_entree , id_sortie   

def compare(voisin_id ,node , nodes , heap ,reverse=False, heap_reverse=[]) :
    voisin_dist=node.neightboors_dist[voisin_id]
    v = nodes[ voisin_id ]

    def HEAP():
        if vpred is None :
            pimped_heap.heappush(heap_choisie,v,reverse)
        else :
            pimped_heap.decrease_key(heap_choisie,v,reverse )

    if not reverse  :
        heap_choisie = heap 
        vpred = v.pred
        if not nodes[voisin_id].closed:
            dist = node.dist + voisin_dist
            if v.dist > dist :
                v.dist = dist
                v.pred = node.id
                HEAP()
    else :
        heap_choisie= heap_reverse 
        vpred=v.reverse_pred
        if not nodes[voisin_id].reverse_closed:
            dist = node.reverse_dist + voisin_dist
            if v.reverse_dist > dist :
                v.reverse_dist = dist
                v.reverse_pred = node.id
                HEAP()

def dijkstra_mono (nodes) : 
    """
    \nAlgorithme de Dijkstra
    \nSortie : Chemin, distance, historique, Temps
    """


    id_entree,id_sortie = definition_entree_sortie(nodes)

    nodes[id_entree].dist = 0
    heap =[nodes[id_entree]]
    history=[]

    t0=time.time()
    while heap :
        history.append((heap[0].id,heap[0].dist))
        node = pimped_heap.heappop(heap)
        node.closed = True
        if node.id == id_sortie :
            T = time.time()-t0
            print("\n\nTERMINATED MONO")
            return (traverse(nodes , id_sortie ), node.dist ,history,T)
        for voisin_id in node.neightboors_dist:
            compare(voisin_id,node,nodes,heap)
    raise NotFound("\nPas de chemin trouvé ")         
def dijkstra_double (nodes) :
    """
    \nAlgorithme de Dijkstra bidirectionnel
    \nSortie : Chemin, distance, historique du sens 1, historique du sens 2, historique global, Temps
    """


    id_entree,id_sortie = definition_entree_sortie(nodes)

    nodes[id_entree].dist = 0
    nodes[id_sortie].reverse_dist = 0
    heap = [nodes[id_entree]]
    heap_reverse = [nodes[id_sortie]]
    history=[]
    history_reverse=[]
    history_total = []

    prec_heap_node = None
    reverse = False

    t0=time.time()

    while heap or heap_reverse:
        
        # conservadtion du rayon de recherche le plus court
        if heap and heap_reverse:
            if heap[0].dist <= heap_reverse[0].reverse_dist :
                if heap[0] == prec_heap_node: # pour ne pas stagner sur ce noeud !
                    history_reverse.append((heap_reverse[0].id,heap_reverse[0].reverse_dist))
                    node = pimped_heap.heappop(heap_reverse,reverse)
                    reverse = True
                else :
                    history.append((heap[0].id,heap[0].dist))
                    node = pimped_heap.heappop(heap)
                    reverse = False
            else:
                history_reverse.append((heap_reverse[0].id,heap_reverse[0].reverse_dist))
                node = pimped_heap.heappop(heap_reverse,reverse)
                reverse = True

        #elif heap :
        #    history.append((heap[0].id,heap[0].dist))
        #    node = pimped_heap.heappop(heap)
        #    reverse = False
        #
        #elif heap_reverse : 
        #    history_reverse.append((heap_reverse[0].id,heap_reverse[0].reverse_dist))
        #    node = pimped_heap.heappop(heap_reverse)
        #    reverse = True

        history_total.append((node.id,node.reverse_dist if reverse else node.dist))
        
        # nouvelle condition d'arrêt, si le noeud est déjà fermé lors du passage de la recherche dans un sens 
        # c'est que la recherche dans l'autre sens l'a déjà trouvé, et donc jointure !
        if node.closed or node.reverse_closed:
            T=time.time()-t0
            print("\n\nTERMINATED DOUBLE")
            
            if reverse :
                d = node.reverse_dist + nodes[node.pred].dist + node.neightboors_dist[node.pred] 
            
            else:
                d = node.dist + nodes[node.reverse_pred].reverse_dist + node.neightboors_dist[node.reverse_pred]  
            
            path = traverse(nodes,node.pred) + [node.id] + traverse(nodes,node.reverse_pred,True)

            #print("sense 1 ", traverse(nodes,node.id),"\nsens2 ",traverse(nodes,node.reverse_pred,True))

            return (path,d,history,history_reverse,history_total,T)

        else :
            if reverse :
                node.reverse_closed = True
            else:
                node.closed = True
            prec_heap_node = node

        for voisin_id in node.neightboors_dist:
            compare(voisin_id,node,nodes,heap,reverse,heap_reverse)

    raise NotFound("\nPas de chemin trouvé ")


if __name__ == '__main__':

    #Démo exam
    
    Maze_file= "/home/hugo/Documents/Enac/Projet info programmes Oral/Labyrinthe.txt"
    Graphic_maze,nodes = maze_converter.get_all(Maze_file)
#    Graphic_maze = maze_converter.graph_regulier
    nodes = maze_converter.node_inventory(Graphic_maze)[0]
    working_lab_mono = Graphic_maze.copy()
    maze_converter.graphics(working_lab_mono)
    chemin,distance,history,T=dijkstra_mono(nodes)
    print("Distance : ",distance,"\nChemin :",chemin)
    maze_converter.update_final(working_lab_mono,chemin)
    maze_converter.graphics(working_lab_mono,history,chemin)

    print("Reset and switch to double")
    working_lab_double = Graphic_maze.copy()
    maze_converter.graphics(working_lab_double)
    Chemin2, Distance2,history2,history2_reverse,h_total,T = dijkstra_double(nodes)
    print("Distance : ",Distance2,"\nChemin :",Chemin2)
    maze_converter.update_final(working_lab_double,Chemin2)
    maze_converter.graphics(working_lab_double,h_total,Chemin2,history_reverse=history2_reverse)





    
