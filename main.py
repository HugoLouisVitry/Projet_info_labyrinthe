import maze_converter
import parcoursmono
import time
import matplotlib.pyplot as plt
import creer_labyrinthe

def chrono(n):
    if n <=1  :
        return " prendre un n plus grand "
    t=[]
    dist = []
    nb_nodes = []
    i=0
    for _ in range(n):
        i+=1
        maze_file = creer_labyrinthe.laby(n,n)
#        maze_file = "/home/hugo/Github/Projet_info_labyrinthe/Labyrinthe.txt"
        nodes = maze_converter.node_inventory(maze_file)[0]
        nb_nodes.append(len(nodes))
        t0=time.time()
        dist.append(parcoursmono.dijkstra_mono(nodes)[1])
        t.append(time.time()-t0)
        print("processing: ",i)

    figure, graphe = plt.subplots(2)
    figure.suptitle(f"Résultats pour {n} labyrinthes de dimensions {n}*{n}")
    graphe[0].set_title("Temps en fct du nb de noeuds")
    graphe[0].scatter(nb_nodes,t)
    plt.grid(True)
    graphe[1].set_title("Temps en fct de la distance")
    graphe[1].scatter(dist,t)
    plt.grid(True)
    A = plt.show()
    return A





if __name__ == "__main__":
    # test du labyrinthe fait main
#    Maze_file = "/home/hugo/Github/Projet_info_labyrinthe/Labyrinthe.txt"
#    Maze,Nodes = maze_converter.get_all(Maze_file)
#
#    maze_converter.graphics(Maze)
#
#    Chemin, Distance = parcoursmono.dijkstra_mono(Nodes)
#
#    maze_converter.update_final(Maze,Chemin)
#    maze_converter.graphics(Maze)
#    plt.figure()
#    plt.plot([i for i in range(100)],[i**2 for i in range(100)])#scatter(nb_nodes,t)
#    plt.show()
    chrono(100)

    