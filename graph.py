import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def createGraph(words):
    unique = np.unique(words, return_counts=True)
    repeated_words = [unique[0][i] for i in range(len(unique[0])) if unique[1][i] > 1]

    G = nx.Graph()
    for i in range(len(words)):
        G.add_node(i)
    for i in range(len(words) - 1):
        G.add_edge(i, i + 1)

    pos = nx.circular_layout(G)
    nx.draw(G, pos)
    plt.show()