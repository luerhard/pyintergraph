
import networkx as nx
import igraph
from graph_tool import Graph

# NetworkX Graphs

def nxg_gnp_random(directed):
    return nx.gnp_random_graph(100, 0.3, seed=1234, directed=directed)

nx_graph_list = [nx.karate_club_graph(), nxg_gnp_random(directed=True), nxg_gnp_random(directed=False)]

# igraph Graphs
def ig_star(directed):
    g = igraph.Graph(directed=directed)
    for i in range(10):
        g.add_vertex(i)
    vertices = [v["name"] for v in g.vs()]
    for i in vertices[1:]:
        g.add_edge(i,0)
    return g

ig_graph_list = [ig_star(directed=False), ig_star(directed=True)]


#graph_tool Graphs

def gt_star(directed):
    g = Graph(directed=directed)
    label_property = g.new_vertex_property("string")
    for i in range(1,11):
        v = g.add_vertex(1)
        label_property[v] = str(i)
    
    g.vp["node_labels"] = label_property
    vertices = g.vertices()
    star_center = next(vertices)
    for j in vertices:
        g.add_edge(star_center, j)

    return g

gt_graph_list = [gt_star(directed=False), gt_star(directed=True)]