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

def compare(reverse , voisin_id ,node , nodes , heap , heap_reverse=[]) :
    if not reverse  :
        heap_choisie = heap 
        node_dist = node.dist
    else :
        heap_choisie= heap_reverse 
        node_dist = node.reverse_dist
    voisin_dist=node.neightboors_dist[voisin_id]
    if not nodes[voisin_id].closed :
               dist = node_dist + voisin_dist
               v = nodes[ voisin_id ]
               v_pred = v.pred if not reverse else v.reverse_pred 
               v_dist = v.dist if not reverse else v.reverse_dist
               if v_dist > dist :
                v_dist = dist
                v_pred = node.id
                if v_pred is None :
                    pimped_heap.heappush( heap_choisie , v )
                 
                else :
                    pimped_heap.decrease_key(heap_choisie , v )
