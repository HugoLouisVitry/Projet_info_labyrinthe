import numpy as np


def create_maze(rows, columns):
            
    test = True
    while test = True and ..:
        
        coord_entry, coord_exit = 0, 0  
        m = np.random.randint(0,2,(rows, columns))
        for i in range(rows):
            for j in range(columns):
                if (i == 0 or i == rows - 1) or (j == 0 or j == columns - 1):
                    m[i][j] = 1
                elif m[i][j] == 2:
                    coord_entry = (i, j)
                elif m[i][j] == 3:
                    coord_exit = (i, j)
        
        
        for i in range(1,rows -1):
            for j in range(1, columns - 1):
                
                


            