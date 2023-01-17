import maze_converter
import parcoursmono
import creer_labyrinthe
import matplotlib.pyplot as plt 
import xlwt

list_dist_max , list_nombre_noeuds = [] , []
Tmono , Tbidi = [] , []
fichier_excel_courbes = xlwt.Workbook()
feuille1 = fichier_excel_courbes.add_sheet('feuille1')
feuille1.write(0,0, 'taille du labyrinthe')
feuille1.write(0,1, 'temps mono')
feuille1.write(0,2, 'temps bidi')

for i in range(30,301) : 
    Maze_file= ("database\{}*{}.txt").format(i,i) #penser à mettre le vrai chemin sur vos pc (ou se trouve database)
    Graphic_maze,nodes = maze_converter.get_all(Maze_file)
    lab = creer_labyrinthe.laby(i,i)
    maze_converter.graphics(Graphic_maze)
    N = len(nodes) #nombre de noeuds pour le labyrinthe généré
    list_nombre_noeuds.append(N)
    Chemin, Distance,history,Tm = parcoursmono.dijkstra_mono(nodes)
    Chemin2, Distance2,history2,history2_reverse,h_total,Tb = parcoursmono.dijkstra_double(nodes)
    Tbidi.append(Tb)
    Tmono.append(Tm)
    list_dist_max.append(Distance)
    feuille1.write(i,0 ,i)
    feuille1.write(i,1 , Tmono)
    feuille1.write(i,1 , Tbidi)


fichier_excel_courbes.save('fichier courbes.xls')
fig  , graph = plt.subplots(2)
plt.subplot(211)
plt.plot( list_dist_max, Tmono , 'o' , label = "Courbe_parcours_mono")
plt.plot( list_dist_max, Tbidi , 'o' , label = "Courbe_parcours_bidirec")
graph[0].set_title('Temps d execution en fonction de la distance parcourue')
plt.legend()

plt.subplot(212)
plt.plot(list_nombre_noeuds, Tmono , 'o' , label = "Courbe_parcours_mono")
plt.plot(list_nombre_noeuds , Tbidi , 'o' ,label = "Courbe_parcours_bidirec")
graph[1].set_title('Temps d execution en fontion du nombre de noeuds')
plt.legend()
plt.show() 