import numpy as np
import random
import maze_converter
import dijkstra
import time

RESET = 1
CHEMIN = 0
MUR = 1
ENTREE = 2
SORTIE = 3
INIT = 4  #(pour initialiser, les chemins non visitées...)

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
            
def make_murs(lignes, colonnes,lab):
    """
    \nChange les cases indéfinies non modifiées en mur
    """
    for i in range(lignes):
        for j in range(colonnes):
            if (lab[i][j] == INIT):
                lab[i][j] = MUR
                
def entree_sortie(lignes, colonnes,lab,mode=0):
    """
    \nPlace l'entrée et la sortie 
    \nMode 0 ( par défaut ) : aléatoirement sur les bords
    \nMode 1 : en haut à gauche, en bas à droite
    \nMode 2 : aléatoirement sur le labyrinthe:
    """
    
    if mode == 1:
        for i in range(lignes):
            if (lab[1][i] == 0):
                lab[0][i] = ENTREE
                break
        for i in range(colonnes-1, 0, -1):
            if (lab[lignes-2][i] == 0):
                lab[lignes-1][i] = SORTIE
                break

    elif not mode:
        e_s_candidates=[]

        for j in range(colonnes):
            if (lab[1][j] == CHEMIN):
                e_s_candidates.append([0,j])
            if (lab[lignes-2][j] == CHEMIN):
                e_s_candidates.append([lignes-1,j])

        for i in range(1,lignes-1):
            if (lab[i][1] == CHEMIN):
                e_s_candidates.append([i,0])
            if (lab[i][colonnes-2] == CHEMIN):
                e_s_candidates.append([i,colonnes-1])

        k=random.choice(e_s_candidates)
        e_s_candidates.remove(k)
        lab[k[0]][k[1]] = ENTREE
        k=random.choice(e_s_candidates)
        lab[k[0]][k[1]] = SORTIE
    else :
        defined = False
        while not defined :
            i = random.randint(0,lignes-1)
            j = random.randint(0,colonnes-1)
            if not lab[i][j]:
                lab[i][j]=ENTREE
                defined =True
        
        defined = False
        while not defined :
            i = random.randint(0,lignes-1)
            j = random.randint(0,colonnes-1)
            if not lab[i][j]:
                lab[i][j]=SORTIE
                defined = True




def creer_lab(lignes, colonnes,mode=0):
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
    
    
    def delete_wall(mur):
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
    
    				# Leftmost cell
                    if (mur[1] != 0): # gauche
                        if (lab[mur[0]][mur[1]-1] != CHEMIN):
                            lab[mur[0]][mur[1]-1] = MUR
                        if ([mur[0], mur[1]-1] not in murs):
                            murs.append([mur[0], mur[1]-1])
    			
                    
                
                delete_wall(mur)
                
                
            
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
                                
                    
                delete_wall(mur)
               
    
                
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
                            
                delete_wall(mur)
                
    
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
                    
        
                delete_wall(mur)
                
        delete_wall(mur)   

    #print(w,"itérations")
    make_murs(lignes, colonnes,lab)
    entree_sortie(lignes, colonnes,lab,mode)
    return lab

def laby(l,c,mode=0):
    """
    \nComplétion des bords
    \nChoix E/S :
    \n  - Mode 0 : sur les bords
    \n  - Mode 1 : en haut à gauche, en bas à droite
    \n  - Mode 2 : aléatoirement sur le labyrinthe:
    """
    lab = creer_lab(l, c,mode)
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

def save_lab(lab=np.array,file_name=str,folder =''):
    """Sauvegarde un labyrinthe sous format fichier texte"""
    l,c = lab.shape

    with open(folder+file_name+'.txt', 'w') as f:
        for i in range(l):
            for j in range(c):    
                f.write(str(lab[i][j]))
            f.write('\n')

def create_database(n,folder,start=30):
    """ 
    \nCrée n-30 labyrinthes de taille 30 à n
    \nPlacée dans "folder", pensez à indique un chemin absolu si le relatif ne marche pas
     """
    if n <= 30 :
        return "\n Please give n > 30 "

    T0 =time.time()
    
    for i in range(start,n+1):
        t0 =time.time()
        lab = laby(i,i)
        save_lab(lab,str(i)+"x"+str(i),folder)
        T = time.time()- t0
        print(f"Execution time for size {i}x{i} : ",round(T,2))

    total_time = time.time()-T0
    print("Done. Total execution time : ",total_time)

if __name__ == "__main__":
    
    # Démo exam
    
    absolute_folder = '/home/hugo/Documents/Enac/Projet info programmes Oral/BDD_lab/'
    #save_lab(laby(600,600,2),"600x600",absolute_folder+'crash/')
    #print("\nSAVED")
    #create_database(300,absolute_folder)
 
    n = int(input("\nChoix de la taille du labyrinthe dans la BDD (entre 30 et 600 ): "))
    u = int(input("\nChoix de la BDD ( 1,2 ou 3): "))
    file = absolute_folder +f'BDD_{u}/' + f"{n}x{n}.txt"
    Graphic_maze,nodes = maze_converter.get_all(file)


    working_lab_mono = Graphic_maze.copy()
    maze_converter.graphics(working_lab_mono)
    chemin,distance,history,T=dijkstra.dijkstra_mono(nodes)
    print("\nDistance : ",distance,"\nTemps :",T)
    maze_converter.update_final(working_lab_mono,chemin)
    maze_converter.graphics(working_lab_mono,history,chemin)

    print("\nReset and switch to double")
    working_lab_double = Graphic_maze.copy()
    maze_converter.graphics(working_lab_double)
    Chemin2, Distance2,history2,history2_reverse,h_total,T2 = dijkstra.dijkstra_double(nodes)
    print("\nDistance : ",Distance2,"\nTemps :",T2)
    maze_converter.update_final(working_lab_double,Chemin2)
    maze_converter.graphics(working_lab_double,h_total,Chemin2,history_reverse=history2_reverse)

#45-100-241

