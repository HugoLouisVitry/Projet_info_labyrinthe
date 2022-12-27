import numpy as np
import random
import maze_converter
import parcoursmono
CHEMIN = 0
MUR = 1
ENTREE = 2
SORTIE = 3
NI_NI = 4  #ni ni(pour initialiser, les chemins non visitées...)

def lab0(lignes, colonnes): #matrice initiale
    return np.random.randint(4, 5, (lignes, colonnes))

def chemins_voisins(mur,lab):
    nb = 0 #nb des chenins voisins
    if (lab[mur[0]-1][mur[1]] == CHEMIN):
        nb += 1
    if (lab[mur[0]+1][mur[1]] == CHEMIN):
        nb += 1
    if (lab[mur[0]][mur[1]-1] == CHEMIN):
        nb +=1
    if (lab[mur[0]][mur[1]+1] == CHEMIN):
        nb += 1
    return nb
            
def make_murs(lignes, colonnes,lab):
    for i in range(lignes):
        for j in range(colonnes):
            if (lab[i][j] == NI_NI):
                lab[i][j] = MUR
                
def entree_sortie(lignes, colonnes,lab):
    for i in range(lignes):
        if (lab[1][i] == CHEMIN):
            lab[0][i] = ENTREE
            break
    for i in range(colonnes-1, 0, -1):
        if (lab[lignes-2][i] == CHEMIN):
            lab[lignes-1][i] = SORTIE
            break
def creer_lab(lignes, colonnes):
    lab = lab0(lignes,colonnes)
    ligne1 = int(random.random()*lignes)
    colonne1 = int(random.random()*colonnes)
    
    if ligne1 == CHEMIN:
        ligne1 += 1
    if ligne1 == lignes-1:
        ligne1 -= 1
    if colonne1 == CHEMIN:
        colonne1 += 1
    if colonne1 == colonnes-1:
        colonne1 -= 1
        
    lab[ligne1][colonne1] = CHEMIN
    murs = []
    murs.append([ligne1-1, colonne1])
    murs.append([ligne1, colonne1-1])
    murs.append([ligne1, colonne1+1])
    murs.append([ligne1+1, colonne1])
    
    lab[ligne1-1][colonne1] = MUR
    lab[ligne1][colonne1-1] = MUR
    lab[ligne1][colonne1+1] = MUR
    lab[ligne1+1][colonne1] = MUR
    
    
    def delete_wall(mur):
        for m in murs:
            if (m[0] == mur[0] and m[1] == mur[1]):
                murs.remove(mur)
    while murs:
        
        mur= murs[int(random.random()*len(murs))-1] #random wall
        
        if mur[1] != CHEMIN:
            if lab[mur[0]][mur[1]-1] == NI_NI and lab[mur[0]][mur[1]+1] == CHEMIN:
                nb_chemins = chemins_voisins(mur,lab)
                if nb_chemins < 2:
                    lab[mur[0]][mur[1]] = CHEMIN
                    
                    if (mur[0] != CHEMIN):
                        if (lab[mur[0]-1][mur[1]] != CHEMIN):
                            lab[mur[0]-1][mur[1]] = MUR
                            if ([mur[0]-1, mur[1]] not in murs):
                                murs.append([mur[0]-1, mur[1]])
                    if (mur[0] != lignes-1):
                        if (lab[mur[0]+1][mur[1]] != CHEMIN):
                            lab[mur[0]+1][mur[1]] = MUR
                        if ([mur[0]+1, mur[1]] not in murs):
                            murs.append([mur[0]+1, mur[1]])
    
    				# Leftmost cell
                    if (mur[1] != CHEMIN):	
                        if (lab[mur[0]][mur[1]-1] != CHEMIN):
                            lab[mur[0]][mur[1]-1] = MUR
                        if ([mur[0], mur[1]-1] not in murs):
                            murs.append([mur[0], mur[1]-1])
    			
                    
                    
                delete_wall(mur)
                
            
        if mur[0] != CHEMIN:
            if lab[mur[0]-1][mur[1]] == NI_NI and  lab[mur[0]+1][mur[1]] == CHEMIN:
                nb_chemins = chemins_voisins(mur,lab)
                if nb_chemins < 2:
                    lab[mur[0]][mur[1]] = CHEMIN
                    
                    if (mur[0] != CHEMIN):
                        if (lab[mur[0]-1][mur[1]] != CHEMIN):
                            lab[mur[0]-1][mur[1]] = MUR
                        if ([mur[0]-1, mur[1]] not in murs):
                            murs.append([mur[0]-1, mur[1]])
                    if (mur[1] != CHEMIN):
                        if (lab[mur[0]][mur[1]-1] != CHEMIN):
                            lab[mur[0]][mur[1]-1] = MUR
                        if ([mur[0], mur[1]-1] not in murs):
                            murs.append([mur[0], mur[1]-1])
                    if (mur[1] != colonnes-1):
                        if (lab[mur[0]][mur[1]+1] != CHEMIN):
                            lab[mur[0]][mur[1]+1] = MUR 
                        if ([mur[0], mur[1]+1] not in murs):
                            murs.append([mur[0], mur[1]+1])
                                
                    
                delete_wall(mur)
               
    
                
        if mur[1] != colonnes -1:
            if lab[mur[0]][mur[1]-1] == CHEMIN and lab[mur[0]][mur[1]+1] == NI_NI:
                nb_chemins = chemins_voisins(mur,lab)
                if nb_chemins < 2:
                    lab[mur[0]][mur[1]] = CHEMIN
                                
                    if (mur[1] != colonnes-1):
                        if (lab[mur[0]][mur[1]+1] != CHEMIN):
                            lab[mur[0]][mur[1]+1] = MUR
                        if ([mur[0], mur[1]+1] not in murs):
                            murs.append([mur[0], mur[1]+1])
                    if (mur[0] != lignes-1):
                        if (lab[mur[0]+1][mur[1]] != CHEMIN):
                            lab[mur[0]+1][mur[1]] = MUR
                        if ([mur[0]+1, mur[1]] not in murs):
                            murs.append([mur[0]+1, mur[1]])
                    if (mur[0] != CHEMIN):	
                        if (lab[mur[0]-1][mur[1]] != CHEMIN):
                            lab[mur[0]-1][mur[1]] = MUR
                        if ([mur[0]-1, mur[1]] not in murs):
                            murs.append([mur[0]-1, mur[1]])
                            
                delete_wall(mur)
                
    
        if mur[0] != lignes -1:
            if lab[mur[0]-1][mur[1]] == CHEMIN and  lab[mur[0]+1][mur[1]] == NI_NI:
                nb_chemins = chemins_voisins(mur,lab)
                if nb_chemins < 2:
                    lab[mur[0]][mur[1]] = CHEMIN
                    
                    if (mur[0] != lignes-1):
                        if (lab[mur[0]+1][mur[1]] != CHEMIN):
                            lab[mur[0]+1][mur[1]] = MUR
                        if ([mur[0]+1, mur[1]] not in murs):
                            murs.append([mur[0]+1, mur[1]])
                    if (mur[1] != CHEMIN):
                        if (lab[mur[0]][mur[1]-1] != CHEMIN):
                            lab[mur[0]][mur[1]-1] = MUR
                        if ([mur[0], mur[1]-1] not in murs):
                            murs.append([mur[0], mur[1]-1])
                    if (mur[1] != colonnes-1):
                        if (lab[mur[0]][mur[1]+1] != CHEMIN):
                            lab[mur[0]][mur[1]+1] = MUR
                        if ([mur[0], mur[1]+1] not in murs):
                            murs.append([mur[0], mur[1]+1])
                    
        
                delete_wall(mur)
                
        delete_wall(mur)
                
    
    make_murs(lignes, colonnes,lab)
    entree_sortie(lignes, colonnes,lab)
    return lab


#lignes = 100
#colonnes = 100
def laby(l,c):
    lab = creer_lab(l, c)

    for i in range(l):
        if lab[i][0] != ENTREE and lab[i][0] != SORTIE:
            lab[i][0] = MUR
        if lab[i][c-1] != ENTREE and lab[i][c-1] != SORTIE:
            lab[i][c-1] =MUR
    for j in range(c):
        if lab[0][j] != ENTREE and lab[0][j] != SORTIE:
            lab[0][j] = MUR
        if lab[l-1][j] != ENTREE and lab[l-1][j] != SORTIE:
            lab[l-1][j] = MUR
    #print(lab)
    return lab



if __name__ == "__main__":
    lab = laby(50,50)
    maze_converter.graphics(lab)
    Nodes = maze_converter.node_inventory(lab)[0]

    Chemin, Distance = parcoursmono.dijkstra_mono(Nodes)

    maze_converter.update_final(lab,Chemin)
    maze_converter.graphics(lab)

    lignes, colonnes = lab.shape
    f = open("lab.txt", 'w')
    for i in range(lignes):
        for j in range(colonnes):
            f.write(str(lab[i][j]))
        f.write('\n')
    
    f.close()


