import networkx as nx
import string
import random

random.seed(1)

def nxg_gnp_random(directed):
    return nx.gnp_random_graph(100, 0.3, seed=1234, directed=directed)

def named_graph(directed, multigraph):
    if directed and not multigraph:
        g = nx.DiGraph()
    elif directed and multigraph:
        g = nx.MultiDiGraph()
    elif not directed and not multigraph:
        g = nx.Graph()
    else:
        g = nx.MultiGraph()

    for c in string.ascii_letters:
        g.add_node(c)
    for _ in range(350):
        u = random.choice(list(g.nodes()))
        v = random.choice(list(g.nodes()))
        g.add_edge(u,v)
    return g
    

def nx_test_graphs():
    yield nxg_gnp_random(directed=True)
    yield nxg_gnp_random(directed=False)
    yield nx.karate_club_graph()
    yield nx.davis_southern_women_graph()
    yield named_graph(directed=False, multigraph=False)
    yield named_graph(directed=False, multigraph=True)
    yield named_graph(directed=True, multigraph=False)
    yield named_graph(directed=True, multigraph=True)
