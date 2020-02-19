import igraph


# igraph Graphs
def ig_star(directed):
    g = igraph.Graph(directed=directed)
    for i in range(10):
        g.add_vertex(i)
        g.vs[i]["name"] = "node" + str(i)
    vertices = [v["name"] for v in g.vs()]

    for i in vertices[1:]:
        g.add_edge(i,0)
    return g


def ig_empty_graph(directed):
    return igraph.Graph(directed=directed)


def igraph_test_graphs():
    yield ig_star(directed=False)
    yield ig_star(directed=True)
    yield igraph.Graph.Tree(50,10)
    yield ig_empty_graph(directed=True)
    yield ig_empty_graph(directed=False)