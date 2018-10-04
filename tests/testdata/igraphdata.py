import igraph

# igraph Graphs
def ig_star(directed):
    g = igraph.Graph(directed=directed)
    for i in range(10):
        g.add_vertex(i)
    vertices = [v["name"] for v in g.vs()]
    for i in vertices[1:]:
        g.add_edge(i,0)
    return g

def igraph_test_graphs():
    yield ig_star(directed=False)
    yield ig_star(directed=True)