import pytest

import networkx as nx
import igraph
from graph_tool import Graph

import pyintergraph

@pytest.fixture
def ig_u():
    g = igraph.Graph(directed=False)
    for i in range(10):
        g.add_vertex(i)
    vertices = [v["name"] for v in g.vs()]
    for i in vertices[1:]:
        g.add_edge(i,0)
    return g

@pytest.fixture
def nx_u():
    return  nx.karate_club_graph()


@pytest.fixture
def gt_u():
    g = Graph(directed=False)
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

def test_nx2igraph_with_labels(nx_u):
    ig_graph = pyintergraph.nx2igraph(nx_u)

    assert list(nx_u.nodes()) == [v["name"] for v in ig_graph.vs()]
    assert [e for e in nx_u.edges()] == [e.tuple for e in ig_graph.es()]

def test_nx2gt_with_labels(nx_u):
    gt_graph = pyintergraph.nx2gt(nx_u, labelname="node_label")

    assert list(gt_graph.vp["node_label"]) == list(nx_u.nodes())
    assert [(e.source(), e.target()) for e in gt_graph.edges()] == list(nx_u.edges())

def test_igraph2nx_with_labels(ig_u):
    nx_graph = pyintergraph.igraph2nx(ig_u)

    assert list(nx_graph.nodes()) == [v["name"] for v in ig_u.vs()]
    assert [e for e in nx_graph.edges()] == [e.tuple for e in ig_u.es()]

def test_igraph2gt_with_labels(ig_u):
    gt_graph = pyintergraph.igraph2gt(ig_u, labelname="node_label")

    assert [v["name"] for v in ig_u.vs()] == list(gt_graph.vp["node_label"])
    assert [e.tuple for e in ig_u.es()] == [(e.source(), e.target()) for e in gt_graph.edges()]

def test_gt2nx_with_labels(gt_u):
    nx_graph = pyintergraph.gt2nx(gt_u, labelname="node_labels")
    nodemap = {v: label for v, label in zip(gt_u.vertices(), gt_u.vp["node_labels"])}

    assert list(gt_u.vp["node_labels"]) == list(nx_graph.nodes())
    assert [(nodemap[e.source()], nodemap[e.target()]) for e in gt_u.edges()] == list(nx_graph.edges())

def test_gt2igraph_with_labels(gt_u):
    ig_graph = pyintergraph.gt2igraph(gt_u, labelname="node_labels", use_labels=True)
    nodemap = {v: label for v, label in zip(gt_u.vertices(), gt_u.vp["node_labels"])}

    assert list(gt_u.vp["node_labels"]) == [v["name"] for v in ig_graph.vs()]

    assert [(nodemap[e.source()], nodemap[e.target()]) for e in gt_u.edges()] == \
            [(nodemap[e.tuple[0]], nodemap[e.tuple[1]]) for e in ig_graph.es()]
