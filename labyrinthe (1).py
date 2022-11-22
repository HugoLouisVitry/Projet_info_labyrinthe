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
            if w[i][j] == 1:
                x1, y1 = j * SIZE, i * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill='black')
            elif w[i][j] == 2 or w[i][j] == 3:
                x1, y1 = j * SIZE, i * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE
                canvas.create_line((x1+x2)/2, y1, (x1+x2)/2, y2, arrow=tk.LAST, fill='red', arrowshape= (12,12,12), width=12)


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












