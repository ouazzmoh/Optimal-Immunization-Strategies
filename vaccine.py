#ouazzmoh
#CPGE Mly Driss 2021


import numpy as np
import matplotlib.pyplot as plt
import random as rd
import networkx as nx
from scipy import interpolate

#---------------Creating the graph-----------------------------
N = 10000                           #Population
BA = nx.barabasi_albert_graph(N,2) #Scale free network using the barabasi albert algorithm


p_i = 0.6   #Infection probability

#------------------Creation des axes----------------------------

points = 20    #Number of simulations
FA_aleatoire = np.zeros(points) #FA : Attacked fraction
FA_vise = np.zeros(points)
FA_conn = np.zeros(points)
FI = np.linspace(0,1,points) #FI : Immunized fraction


#---------------Spread of the pandemic--------------------

def percolation_graphe(G,p):
    H = nx.Graph()   #Creating empty graph
    H.add_nodes_from(G.nodes())  #adding all nodes to the new graph (The edges are not added)
    for arete in G.edges():    #For a certain probability connect nodes
        if rd.random()<p:
            H.add_edge(*arete)
    return H

def taille_epidemie(G, p):
    H = percolation_graphe(G, p)
    composantes = nx.connected_components(H)
    taille = 0
    for c in composantes:
        if len(c) > taille:
            taille = len(c)
    fraction_attacke = float(taille)/G.order()

    return fraction_attacke

#------------------Sorting the graph-------------------------
def fusion(liste1,liste2):
    liste=[]
    i,j=0,0
    while i<len(liste1)and j<len(liste2):
        if liste1[i][1]>=liste2[j][1]: #C'est un tri descendant
            liste.append(liste1[i])
            i+=1
        else:
            liste.append(liste2[j])
            j+=1
    if i < len(liste1): liste.extend(liste1[i:])
    if j < len(liste2): liste.extend(liste2[j:])
    return liste


def tri_fusion(liste):    #liste des tuples
    if len(liste)<2:    return liste
    milieu=len(liste)//2
    liste1=tri_fusion(liste[:milieu])
    liste2=tri_fusion(liste[milieu:])
    return fusion(liste1,liste2)

def tri_graphe(G):
    L = list(G.degree)
    return tri_fusion(L)

#------------------Different immunization strategies------------------

def immunisation_aleatoire(G,f_i):
    G = G.copy()
    A_immuniser = rd.sample(list(G.nodes),int(N * f_i))
    G.remove_nodes_from(A_immuniser)
    return taille_epidemie(G,p_i)

def immunisation_vise(G,f_i):
    G = G.copy()
    G_trie = tri_graphe(G)  #Liste triée de la forme [(noeud, degree)] (tri)
    A_immuniser = []
    for i in range(int(f_i*N)): A_immuniser.append(G_trie[i][0])
    G.remove_nodes_from(A_immuniser)
    return taille_epidemie(G,p_i)

def immunisation_par_connaissance(G,f_i):
    G = G.copy()
    p = rd.random()
    choisi = rd.sample(list(G.nodes),int(p*N))
    N_immunise = int(N*f_i)
    A_immuniser = []
    while N_immunise > 1:
        for noeud in choisi:
            voisins = list(G.neighbors(noeud))
            nv = len(voisins)
            H = rd.randint(0,N_immunise)
            if nv >= H:
                L = rd.sample(voisins, H)
                N_immunise = N_immunise - H
            else:
                L = rd.sample(voisins, nv)
                N_immunise = N_immunise - nv
            A_immuniser.extend(L)
    G.remove_nodes_from(A_immuniser)
    return taille_epidemie(G,p_i)

#----------------Simulating the spread----------------------
for i in range(points-1):
    f_i = FI[i]
    FA_aleatoire[i] = immunisation_aleatoire(BA,f_i)
    FA_vise[i] = immunisation_vise(BA,f_i)
    FA_conn[i] = immunisation_par_connaissance(BA,f_i)

#-----------------------Interpolation------------------------------

x = FI
y1,y2,y3 = FA_aleatoire, FA_vise, FA_conn
f1 = interpolate.interp1d(x,y1,kind = "quadratic")
f2 = interpolate.interp1d(x,y2,kind = "quadratic")
f3 = interpolate.interp1d(x,y3,kind = "quadratic")
xn = np.linspace(0,1,1000)
yn1,yn2,yn3 = f1(xn),f2(xn),f3(xn)

#--------------------------Plotting---------------------------------
plt.plot(x,y1,'or')
plt.plot(xn,yn1,'--r', label = "Immunisation aléatoire")
plt.plot(x,y2,'ob')
plt.plot(xn,yn2,'-.b', label ="Immunisation visée" )
plt.plot(x,y3,'og')
plt.plot(xn,yn3,'-g', label = "Immunisation par connaissances" )
plt.xlabel("fraction immunisée")
plt.ylabel("fraction infectée")
plt.title("Les méthodes d'immunisation")
plt.legend()
plt.grid()
plt.show()
