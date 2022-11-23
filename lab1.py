import tkinter as tk
import numpy as np

SIZE = None

def matrix(file):
    #convert a file into matrix
    
    f = open(file, 'r')
    lines = f.readlines()
    rows, columns = len(lines),len(lines[0])-1
    m = np.random.randint(0,1,(rows, columns))
    for i in range(rows):
        for j in range(columns):
            if lines[i][j] == 'E':
                m[i][j] = 2
            elif lines[i][j] == 'S':
                m[i][j] = 3
            else : 
                m[i][j] = lines[i][j]
                
    return  m

def draw(canvas, w):
    canvas.delete(tk.ALL)
    for i in range(len(w)):
        for j in range(len(w[0])):
            x1, y1 = j * SIZE, i * SIZE
            x2, y2 = x1 + SIZE, y1 + SIZE
            
            if w[i][j] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill='black')
                
            elif w[i][j] == 2:
                if i == 0 and j != 0:
                    canvas.create_line((x1+x2)/2, y1, (x1+x2)/2, y2, arrow=tk.LAST, fill='red', arrowshape= (12,12,12), width=12)
                elif i == len(w) -1 and j != 0:
                    canvas.create_line((x1+x2)/2, y2, (x1+x2)/2, y1, arrow=tk.LAST, fill='red', arrowshape= (12,12,12), width=12)
                elif j == 0 and i != 0:
                    canvas.create_line(x1, (y1+y2)/2, x2, (y1+y2)/2, arrow=tk.LAST, fill='red', arrowshape= (12,12,12), width=12)
                elif j == len(w[0]) and i != 0:
                    canvas.create_line(x2, (y1+y2)/2, x1, (y1+y2)/2, arrow=tk.LAST, fill='red', arrowshape= (12,12,12), width=12)
                    
            elif w[i][j] == 3:
                if i == len(w) - 1 and j != 0:
                    canvas.create_line((x1+x2)/2, y1, (x1+x2)/2, y2, arrow=tk.LAST, fill='red', arrowshape= (12,12,12), width=12)
                elif i == 0 and j!= 0:
                    canvas.create_line((x1+x2)/2, y2, (x1+x2)/2, y1, arrow=tk.LAST, fill='red', arrowshape= (12,12,12), width=12)
                elif j == len(w[0]) and i != 0:
                    canvas.create_line(x1, (y1+y2)/2, x2, (y1+y2)/2, arrow=tk.LAST, fill='red', arrowshape= (12,12,12), width=12)
                elif j == 0 and i != 0:
                    canvas.create_line(x2, (y1+y2)/2, x1, (y1+y2)/2, arrow=tk.LAST, fill='red', arrowshape= (12,12,12), width=12)
                    
                


if __name__ == '__main__':
    
    lab = matrix("Labyrinthe.txt") # depends on where the file is
    rows, columns = np.shape(lab)
    window = tk.Tk()
    window.title("Labyrinthe 1")
    SIZE = min(700 // rows, 800 // columns)
    canvas = tk.Canvas(window, width=SIZE*columns, height=SIZE*rows, bg='white')
    canvas.pack()
    canvas.focus_set()
    canvas.bind('q', lambda _: window.destroy())
    draw(canvas, lab)
    window.mainloop()



