import graph_tool
from graph_tool import generation
import random

def gt_star(directed):
    g = graph_tool.Graph(directed=directed)
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

def circular_graph(directed):
    g = generation.circular_graph(25, 3, directed=directed)
    label_property = g.new_vertex_property("string")

    for i, v in enumerate(g.vertices(), 100):
        label_property[v] = str(i)

    g.vp["node_labels"] = label_property

    return g


def gt_test_graphs():
    yield gt_star(directed=False)
    yield gt_star(directed=True)
    yield circular_graph(directed=True)
    yield circular_graph(directed=False)