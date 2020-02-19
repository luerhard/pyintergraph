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


def nxg_dict_node_attributes(directed):
    if directed:
        g = nx.DiGraph()
    else:
        g = nx.Graph()

    for i in range(1,5):
        g.add_node(i, **{"my_number_minus_one": i-1})
    
    g.add_edges_from([(1,2), (4,3), (2,1), (3,2)])

    return g

def nxg_without_edges(directed):
    g = nx.Graph()
    g.add_node(1)
    g.add_node(12)

    return g

def nxg_list_attributes(directed):
    if directed:
        g = nx.DiGraph()
    else:
        g = nx.Graph()

    for i in range(1,5):
        for j in range(i):
            g.add_node(i, **{"attr_list": [1 for _ in range(j)]})

    g.add_edges_from([(1, 2), (4, 3), (2, 1), (3, 2)])

    return g

def nx_empty_graph():
    return nx.Graph()


def nx_single__vector_float_attr():
    g = nx.Graph()
    g.add_node(1, attr=[1.322])
    return g

def nx_single_vector_str_attr():
    g = nx.Graph()
    g.add_node(1, attr=["attribute"])
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
    yield nxg_dict_node_attributes(directed=True)
    yield nxg_dict_node_attributes(directed=False)
    yield nxg_without_edges(directed=True)
    yield nxg_without_edges(directed=True)
    yield nx_empty_graph()
    yield nx_single__vector_float_attr()
    yield nx_single_vector_str_attr()