import networkx as nx

def nxg_gnp_random(directed):
    return nx.gnp_random_graph(100, 0.3, seed=1234, directed=directed)

def nx_test_graphs():
    yield nxg_gnp_random(directed=True)
    yield nxg_gnp_random(directed=False)
    yield nx.karate_club_graph()
    yield nx.davis_southern_women_graph()