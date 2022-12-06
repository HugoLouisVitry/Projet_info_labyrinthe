import numpy as np
import random


#0 chemin
#1 mur
#2 entree
#3 sortie
#4 ni ni(pour initialiser, les chemins non visitées...)


def lab0(lignes, colonnes): #☺initialiser la matrice
    return np.random.randint(4, 5, (lignes, colonnes))
 
def chemins_voisins(mur):
    nb = 0
    if (lab[mur[0]-1][mur[1]] == 0):
        nb += 1
    elif (lab[mur[0]+1][mur[1]] == 0):
        nb += 1
    elif (lab[mur[0]][mur[1]-1] == 0):
        nb +=1
    elif (lab[mur[0]][mur[1]+1] == 0):
        nb += 1
    return nb
            
def creer_mur(lignes, colonnes):
    for i in range(lignes):
        for j in range(colonnes):
            if (lab[i][j] == 4):
                lab[i][j] = 1
                
def entree_sortie(lignes, colonnes):
    for i in range(lignes):
        if (lab[1][i] == 0):
            lab[0][i] = 2
            break
    for i in range(colonnes-1, 0, -1):
        elif (lab[lignes-2][i] == 0):
            lab[lignes-1][i] = 3
            break
def creer_lab(lignes, colonnes):
            
    ligne1 = int(random.random()*lignes)
    colonne1 = int(random.random()*colonnes)
    
    if ligne1 == 0:
        ligne1 += 1
    elif ligne1 == lignes-1:
        ligne1 -= 1
    elif colonne1 == 0:
        colonne1 += 1
    elif colonne1 == colonnes-1:
        colonne1 -= 1
        
    lab[ligne1][colonne1] = 0
    murs = []
    murs.append([ligne1-1, colonne1])
    murs.append([ligne1, colonne1-1])
    murs.append([ligne1, colonne1+1])
    murs.append([ligne1+1, colonne1])
    
    lab[ligne1-1][colonne1] = 1
    lab[ligne1][colonne1-1] = 1
    lab[ligne1][colonne1+1] = 1
    lab[ligne1+1][colonne1] = 1
    
    
    def delete_wall(mur):
        for wall in murs:
            if (wall[0] == mur[0] and wall[1] == mur[1]):
                murs.remove(wall)
    while murs:
        
        mur = murs[int(random.random()*len(murs))-1] #un mur aleatoire
        
        if mur[1] != 0:
            if lab[mur[0]][mur[1]-1] == 4 and lab[mur[0]][mur[1]+1] == 0:
                nb = chemins_voisins(mur)
                if nb < 2:
                    lab[mur[0]][mur[1]] = 0
                    
                    if (mur[0] != 0):
                        if (lab[mur[0]-1][mur[1]] != 0):
                            lab[mur[0]-1][mur[1]] = 1
                            if ([mur[0]-1, mur[1]] not in murs):
                                murs.append([mur[0]-1, mur[1]])
                    elif (mur[0] != lignes-1):
                        if (lab[mur[0]+1][mur[1]] != 0):
                            lab[mur[0]+1][mur[1]] = 1
                        elif ([mur[0]+1, mur[1]] not in murs):
                            murs.append([mur[0]+1, mur[1]])
    
    				# Leftmost cell
                    elif (mur[1] != 0):	
                        if (lab[mur[0]][mur[1]-1] != 0):
                            lab[mur[0]][mur[1]-1] = 1
                        elif ([mur[0], mur[1]-1] not in murs):
                            murs.append([mur[0], mur[1]-1])
    			
                    
                    
                delete_wall(mur)
               
            
        elif mur[0] != 0:
            if lab[mur[0]-1][mur[1]] == 4 and  lab[mur[0]+1][mur[1]] == 0:
                nb = chemins_voisins(mur)
                if nb < 2:
                    lab[mur[0]][mur[1]] = 0
                    
                    if (mur[0] != 0):
                        if (lab[mur[0]-1][mur[1]] != 0):
                            lab[mur[0]-1][mur[1]] = 1
                        elif ([mur[0]-1, mur[1]] not in murs):
                            murs.append([mur[0]-1, mur[1]])
                    elif (mur[1] != 0):
                        if (lab[mur[0]][mur[1]-1] != 0):
                            lab[mur[0]][mur[1]-1] = 1
                        elif ([mur[0], mur[1]-1] not in murs):
                            murs.append([mur[0], mur[1]-1])
                    elif (mur[1] != colonnes-1):
                        if (lab[mur[0]][mur[1]+1] != 0):
                            lab[mur[0]][mur[1]+1] = 1 
                        elif ([mur[0], mur[1]+1] not in murs):
                            murs.append([mur[0], mur[1]+1])
                                
                    
                delete_wall(mur)
               
    
                
        elif mur[1] != colonnes -1:
            if lab[mur[0]][mur[1]-1] == 0 and lab[mur[0]][mur[1]+1] == 4:
                nb = chemins_voisins(mur)
                if nb < 2:
                    lab[mur[0]][mur[1]] = 0
                                
                    if (mur[1] != colonnes-1):
                        if (lab[mur[0]][mur[1]+1] != 0):
                            lab[mur[0]][mur[1]+1] = 1
                        elif ([mur[0], mur[1]+1] not in murs):
                            murs.append([mur[0], mur[1]+1])
                    elif (mur[0] != lignes-1):
                        if (lab[mur[0]+1][mur[1]] != 0):
                            lab[mur[0]+1][mur[1]] = 1
                        elif ([mur[0]+1, mur[1]] not in murs):
                            murs.append([mur[0]+1, mur[1]])
                    elif (mur[0] != 0):	
                        if (lab[mur[0]-1][mur[1]] != 0):
                            lab[mur[0]-1][mur[1]] = 1
                        elif ([mur[0]-1, mur[1]] not in murs):
                            murs.append([mur[0]-1, mur[1]])
                            
                delete_wall(mur)
               
    
        elif mur[0] != lignes -1:
            if lab[mur[0]-1][mur[1]] == 0 and  lab[mur[0]+1][mur[1]] == 4:
                nb = chemins_voisins(mur)
                if nb < 2:
                    lab[mur[0]][mur[1]] = 0
                    
                    if (mur[0] != lignes-1):
                        if (lab[mur[0]+1][mur[1]] != 0):
                            lab[mur[0]+1][mur[1]] = 1
                        elif ([mur[0]+1, mur[1]] not in murs):
                            murs.append([mur[0]+1, mur[1]])
                    elif (mur[1] != 0):
                        if (lab[mur[0]][mur[1]-1] != 1):
                            lab[mur[0]][mur[1]-1] = 0
                        elif ([mur[0], mur[1]-1] not in murs):
                            murs.append([mur[0], mur[1]-1])
                    elif (mur[1] != colonnes-1):
                        if (lab[mur[0]][mur[1]+1] != 0):
                            lab[mur[0]][mur[1]+1] = 1
                        elif ([mur[0], mur[1]+1] not in murs):
                            murs.append([mur[0], mur[1]+1])
                    
        
                delete_wall(mur)
                
        delete_wall(mur)
                
    
    creer_mur(lignes, colonnes)
    entree_sortie(lignes, colonnes)
    
    
    


lignes = 5
colonnes = 5
lab = lab0(lignes, colonnes)
creer_lab(lignes, colonnes)

l,c= lab.shape



#def walll(lab):
#    l,c= lab.shape
for i in range(l):
    if lab[i][0] != 2 and lab[i][0] != 3:
        lab[i][0] = 1
    if lab[i][c-1] != 2 and lab[i][c-1] != 3:
        lab[i][c-1] =1
for j in range(c):
    if lab[0][j] != 2 and lab[0][j] != 3:
        lab[0][j] = 1
    if lab[l-1][j] != 2 and lab[l-1][j] != 3:
        lab[l-1][j] = 1
    #return lab
  

print(lab)

f = open("lab.txt", 'w')
for i in range(lignes):
    for j in range(colonnes):
        f.write(str(lab[i][j]))
    f.write('\n')

f.close()
    



            

    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
