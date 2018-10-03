import pytest

import networkx as nx
import igraph

import pyintergraph

@pytest.fixture
def iG_u():
    g = igraph.Graph(directed=False)
    for i in range(10):
        g.add_vertex(i)
    vertices = [v["name"] for v in g.vs()]
    for i in vertices[1:]:
        g.add_edge(i,0)
    return g

def test_nx2igraph():
    nxG = nx.karate_club_graph()
    iG = pyintergraph.nx2igraph(nxG)

    assert list(nxG.nodes()) == [v["name"] for v in iG.vs()]
    assert [e for e in nxG.edges()] == [e.tuple for e in iG.es()]

def test_igraph2nx_undirected(iG_u):
    nxG = pyintergraph.igraph2nx(iG_u)

    assert list(nxG.nodes()) == [v["name"] for v in iG_u.vs()]
    assert [e for e in nxG.edges()] == [e.tuple for e in iG_u.es()]

def test_igraph2gt_undirected(iG_u):
    gtG = pyintergraph.igraph2gt(iG_u, labelname="node_label")

    assert [v["name"] for v in iG_u.vs()] == list(gtG.vp["node_label"])
    assert [e.tuple for e in iG_u.es()] == [(e.source(), e.target()) for e in gtG.edges()]