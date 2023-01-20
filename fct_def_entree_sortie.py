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