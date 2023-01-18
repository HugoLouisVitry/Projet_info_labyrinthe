import numpy as np
import random
import maze_converter
import parcoursmono
import time
RESET = 1
CHEMIN = 0
MUR = 1
ENTREE = 2
SORTIE = 3
INIT = 4  #ni ni(pour initialiser, les chemins non visitées...)

def lab0(lignes, colonnes): 
    """
    \nMatrice initiale de cases indéfinies
    """
    return np.random.randint(4, 5, (lignes, colonnes))

#matrice des directions de voisinage [ligne,colone,position physique 0 haut, 1 gauche 2 droite,3 bas]
coord_neightboor = np.array([       [-1,+0,0],
                             [+0,-1,1],       [+0,1,2],
                                    [+1,+0,3]   ])

def chemins_voisins(mur,lab):
    """
    \nCompte le nombre de chemins voisins existant
    """
    nb = 0 #nb des chemins voisins
    # optimisé
    for cn in coord_neightboor:
        if (lab[mur[0]+cn[0]][mur[1]+cn[1]] == CHEMIN):
            nb += 1
    return nb
            
def creer_murs(lignes, colonnes,lab):
    """
    \nChange les cases indéfinies non modifiées en mur
    """
    for i in range(lignes):
        for j in range(colonnes):
            if (lab[i][j] == INIT):
                lab[i][j] = MUR
def entree_sortie(lignes, colonnes,lab):
    for i in range(lignes):
        if (lab[1][i] == 0):
            lab[0][i] = ENTREE
            break
    for i in range(colonnes-1, 0, -1):
        if (lab[lignes-2][i] == 0):
            lab[lignes-1][i] = SORTIE
            break                


def creer_lab(lignes, colonnes):
    """
    \nCreation intégrale aléatoire du labyrinthe
    """
    lab = lab0(lignes,colonnes)
    ligne1 = int(random.random()*lignes)
    colonne1 = int(random.random()*colonnes)
    
    # on garde les bords comme des murs
    if ligne1 == 0:
        ligne1 += 1
    if ligne1 == lignes-1:
        ligne1 -= 1
    if colonne1 == 0:
        colonne1 += 1
    if colonne1 == colonnes-1:
        colonne1 -= 1

    lab[ligne1][colonne1] = CHEMIN
    #maze_converter.graphics(lab)
    murs = []
    murs.append([ligne1-1, colonne1])
    murs.append([ligne1, colonne1-1])
    murs.append([ligne1, colonne1+1])
    murs.append([ligne1+1, colonne1])
    
    lab[ligne1-1][colonne1] = MUR
    lab[ligne1][colonne1-1] = MUR
    lab[ligne1][colonne1+1] = MUR
    lab[ligne1+1][colonne1] = MUR
    #maze_converter.graphics(lab)
    
    
    def supp_mur(mur):
        for m in murs:
            if (m[0] == mur[0] and m[1] == mur[1]):
                murs.remove(mur)
    w=0
    while murs:
        
        w+=1
        #maze_converter.graphics(lab)
        mur = murs[int(random.random()*len(murs))-1] #random wall

        if mur[1] != 0: # gauche
            if lab[mur[0]][mur[1]-1] == INIT and lab[mur[0]][mur[1]+1] == CHEMIN:
                nb_chemins = chemins_voisins(mur,lab)
                if nb_chemins < 2:
                    lab[mur[0]][mur[1]] = CHEMIN
                    
                    if (mur[0] != 0): #haut
                        if (lab[mur[0]-1][mur[1]] != CHEMIN):
                            lab[mur[0]-1][mur[1]] = MUR
                        if ([mur[0]-1, mur[1]] not in murs):
                            murs.append([mur[0]-1, mur[1]])
                    if (mur[0] != lignes-1): # bas
                        if (lab[mur[0]+1][mur[1]] != CHEMIN):
                            lab[mur[0]+1][mur[1]] = MUR
                        if ([mur[0]+1, mur[1]] not in murs):
                            murs.append([mur[0]+1, mur[1]])
    
    				
                    if (mur[1] != 0): # gauche
                        if (lab[mur[0]][mur[1]-1] != CHEMIN):
                            lab[mur[0]][mur[1]-1] = MUR
                        if ([mur[0], mur[1]-1] not in murs):
                            murs.append([mur[0], mur[1]-1])
    			
                supp_mur(mur)
                
                
            
        if mur[0] != 0:# haut
            if lab[mur[0]-1][mur[1]] == INIT and  lab[mur[0]+1][mur[1]] == CHEMIN:
                nb_chemins = chemins_voisins(mur,lab)
                if nb_chemins < 2:
                    lab[mur[0]][mur[1]] = CHEMIN
                    
                    if (mur[0] != 0): # haut
                        if (lab[mur[0]-1][mur[1]] != CHEMIN):
                            lab[mur[0]-1][mur[1]] = MUR
                        if ([mur[0]-1, mur[1]] not in murs):
                            murs.append([mur[0]-1, mur[1]])
                    if (mur[1] != 0): # gauche
                        if (lab[mur[0]][mur[1]-1] != CHEMIN):
                            lab[mur[0]][mur[1]-1] = MUR
                        if ([mur[0], mur[1]-1] not in murs):
                            murs.append([mur[0], mur[1]-1])
                    if (mur[1] != colonnes-1): # droite
                        if (lab[mur[0]][mur[1]+1] != CHEMIN):
                            lab[mur[0]][mur[1]+1] = MUR 
                        if ([mur[0], mur[1]+1] not in murs):
                            murs.append([mur[0], mur[1]+1])
                                
                    
                supp_mur(mur)
               
    
                
        if mur[1] != colonnes -1:# droite
            if lab[mur[0]][mur[1]-1] == CHEMIN and lab[mur[0]][mur[1]+1] == INIT:
                nb_chemins = chemins_voisins(mur,lab)
                if nb_chemins < 2:
                    lab[mur[0]][mur[1]] = CHEMIN
                                
                    if (mur[1] != colonnes-1): # droite
                        if (lab[mur[0]][mur[1]+1] != CHEMIN):
                            lab[mur[0]][mur[1]+1] = MUR
                        if ([mur[0], mur[1]+1] not in murs):
                            murs.append([mur[0], mur[1]+1])
                    if (mur[0] != lignes-1): # bas
                        if (lab[mur[0]+1][mur[1]] != CHEMIN):
                            lab[mur[0]+1][mur[1]] = MUR
                        if ([mur[0]+1, mur[1]] not in murs):
                            murs.append([mur[0]+1, mur[1]])
                    if (mur[0] != 0):	#haut
                        if (lab[mur[0]-1][mur[1]] != CHEMIN):
                            lab[mur[0]-1][mur[1]] = MUR
                        if ([mur[0]-1, mur[1]] not in murs):
                            murs.append([mur[0]-1, mur[1]])
                            
                supp_mur(mur)
                
    
        if mur[0] != lignes -1:# bas
            if lab[mur[0]-1][mur[1]] == CHEMIN and  lab[mur[0]+1][mur[1]] == INIT:
                nb_chemins = chemins_voisins(mur,lab)
                if nb_chemins < 2:
                    lab[mur[0]][mur[1]] = CHEMIN
                    
                    if (mur[0] != lignes-1): #bas
                        if (lab[mur[0]+1][mur[1]] != CHEMIN):
                            lab[mur[0]+1][mur[1]] = MUR
                        if ([mur[0]+1, mur[1]] not in murs):
                            murs.append([mur[0]+1, mur[1]])
                    if (mur[1] != 0):#gauche
                        if (lab[mur[0]][mur[1]-1] != CHEMIN):
                            lab[mur[0]][mur[1]-1] = MUR
                        if ([mur[0], mur[1]-1] not in murs):
                            murs.append([mur[0], mur[1]-1])
                    if (mur[1] != colonnes-1): #droite
                        if (lab[mur[0]][mur[1]+1] != CHEMIN):
                            lab[mur[0]][mur[1]+1] = MUR
                        if ([mur[0], mur[1]+1] not in murs):
                            murs.append([mur[0], mur[1]+1])
                    
        
                supp_mur(mur)
                
        supp_mur(mur)   

    #print(w,"itérations")
    creer_murs(lignes, colonnes,lab)
    entree_sortie(lignes, colonnes,lab)
    return lab


#lignes = 100
#colonnes = 100
def laby(l,c):
    """
    Complétion des bords
    """
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
    
    lignes, colonnes = 20,30
    t0=time.time()
    lab = laby(lignes,colonnes)
    working_lab = lab.copy()
    print("Laby Execution time",round(time.time()-t0,10))
    
    maze_converter.graphics(working_lab)
    t0=time.time()
    Nodes = maze_converter.node_inventory(working_lab)[0]
    print("Node inventory Execution time",round(time.time()-t0,10))



    Chemin, Distance,history,T = parcoursmono.dijkstra_mono(Nodes)
    print("Simple Dijkstra Execution time",round(T,10))

    
    print("Chemin mono ",Chemin)
    #maze_converter.update_final(working_lab,Chemin)
    #maze_converter.graphics(working_lab,history,Chemin)
    
    working_lab = lab.copy()

    Chemin2, Distance2,history2,history2_reverse,h_total,T = parcoursmono.dijkstra_double(Nodes)
    print("Double Dijkstra Execution time",round(T,10))

    print("Chemin double ",Chemin2)

    #maze_converter.graphics(working_lab,reset=RESET)

    #maze_converter.update_final(working_lab,Chemin2)
    #maze_converter.graphics(working_lab)
    #maze_converter.graphics(working_lab,h_total,Chemin2,history_reverse=history2_reverse)
    lab = laby(lignes,colonnes)
    Nodes = maze_converter.node_inventory(working_lab)[0]
    Chemin, Distance,history,T = parcoursmono.dijkstra_mono(Nodes)
    Chemin2, Distance2,history2,history2_reverse,h_total,T = parcoursmono.dijkstra_double(Nodes)

    #lignes, colonnes = lab.shape
    #f = open("lab.txt", 'w')
    #for i in range(lignes):
    #    for j in range(colonnes):
    #        f.write(str(lab[i][j]))
    #    f.write('\n')
    
    #f.close()
    #lab = creer_lab(15,15)
    #maze_converter.graphics(lab)