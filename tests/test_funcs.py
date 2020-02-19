import pytest

import pyintergraph

from .testdata.networkxdata import *
from .testdata.igraphdata import *
from .testdata.gtdata import *

#Tests
@pytest.mark.nx
@pytest.mark.ig
@pytest.mark.parametrize("nx_graph", nx_test_graphs())
def test_nx2igraph_with_labels(nx_graph):
    ig_graph = pyintergraph.nx2igraph(nx_graph)
    nodemap = {v.index: v["name"] for v in ig_graph.vs()}

    assert list(nx_graph.nodes()) == [v["name"] for v in ig_graph.vs()]
    assert [e for e in nx_graph.edges()] == \
            [(nodemap[e.tuple[0]], nodemap[e.tuple[1]])  for e in ig_graph.es()]

@pytest.mark.nx
@pytest.mark.gt
@pytest.mark.parametrize("nx_graph", nx_test_graphs())
def test_nx2gt(nx_graph):
    gt_graph = pyintergraph.nx2gt(nx_graph, labelname="node_label")
    try:
        next(gt_graph.vertices())
        nodemap = {v: label for v, label in zip(gt_graph.vertices(), gt_graph.vp["node_label"])}
        assert list(gt_graph.vp["node_label"]) == list(nx_graph.nodes())
    except StopIteration:
        nodemap = {}
        assert list(nx_graph.nodes()) == []


    if not nx_graph.is_directed():
        assert set([frozenset((nodemap[e.source()], nodemap[e.target()])) for e in gt_graph.edges()]) == \
                set([frozenset(e) for e in nx_graph.edges()])
    else:
        assert [(nodemap[e.source()], nodemap[e.target()]) for e in gt_graph.edges()] == list(nx_graph.edges())

@pytest.mark.nx
@pytest.mark.gt
@pytest.mark.parametrize("nx_graph", nx_test_graphs())
def test_nx2gt_without_labels(nx_graph):
    gt_graph = pyintergraph.nx2gt(nx_graph)
    nodemap = {v: i for v, i in zip(nx_graph.nodes(), range(len(nx_graph.nodes())))}

    assert list(gt_graph.get_vertices()) == list(nodemap.values())
    if not nx_graph.is_directed():
        assert set([frozenset((e.source(), e.target())) for e in gt_graph.edges()]) == \
                set([frozenset((nodemap[u], nodemap[v])) for u,v in nx_graph.edges()])
    else:
        assert [(e.source(), e.target()) for e in gt_graph.edges()] == \
                list((nodemap[u], nodemap[v]) for u, v in nx_graph.edges())

@pytest.mark.ig
@pytest.mark.nx
@pytest.mark.parametrize("ig_graph", igraph_test_graphs())
def test_igraph2nx(ig_graph):
    nx_graph = pyintergraph.igraph2nx(ig_graph)

    if "name" in ig_graph.vertex_attributes():
        nodemap = {v.index: v["name"] for v in ig_graph.vs()}
        assert list(nx_graph.nodes()) == [v["name"] for v in ig_graph.vs()]
    else:
        nodemap = {v.index: v.index for v in ig_graph.vs()}
        assert list(nx_graph.nodes()) == [v.index for v in ig_graph.vs()]

    assert [e for e in nx_graph.edges()] == \
            [(nodemap[e.tuple[0]], nodemap[e.tuple[1]])  for e in ig_graph.es()]


@pytest.mark.ig
@pytest.mark.gt
@pytest.mark.parametrize("ig_graph", igraph_test_graphs())
def test_igraph2gt(ig_graph):
    gt_graph = pyintergraph.igraph2gt(ig_graph, labelname="node_label")
    try:
        next(gt_graph.vertices())
    except StopIteration:
        assert ig_graph.vcount() == len(list(gt_graph.vertices()))
        assert ig_graph.ecount() == len(list(gt_graph.edges()))
        return

    if "name" in ig_graph.vertex_attributes():
        assert [v["name"] for v in ig_graph.vs()] == list(gt_graph.vp["node_label"])
    else:
        assert [v.index for v in ig_graph.vs()] == list(gt_graph.vp["node_label"])
    assert [e.tuple for e in ig_graph.es()] == [(e.source(), e.target()) for e in gt_graph.edges()]

@pytest.mark.gt
@pytest.mark.nx
@pytest.mark.parametrize("gt_graph", gt_test_graphs())
def test_gt2nx(gt_graph):
    if "node_labels" in gt_graph.vp:
        nx_graph = pyintergraph.gt2nx(gt_graph, labelname="node_labels")
        nodemap = {v: label for v, label in zip(gt_graph.get_vertices(), gt_graph.vp["node_labels"])}

        assert list(gt_graph.vp["node_labels"]) == list(nx_graph.nodes())
        if not nx_graph.is_directed():
            assert set([frozenset((nodemap[e.source()], nodemap[e.target()])) for e in gt_graph.edges()]) == \
                    set([frozenset(e) for e in nx_graph.edges()])
        else:
            assert [(nodemap[e.source()], nodemap[e.target()]) for e in gt_graph.edges()] == list(nx_graph.edges())
    else:
        nx_graph = pyintergraph.gt2nx(gt_graph)

        assert list(gt_graph.get_vertices()) == list(nx_graph.nodes())
        if not nx_graph.is_directed():
            assert set([frozenset((e.source(), e.target())) for e in gt_graph.edges()]) == \
                    set([frozenset(e) for e in nx_graph.edges()])
        else:
            assert [(e.source(), e.target()) for e in gt_graph.edges()] == list(nx_graph.edges())

@pytest.mark.gt
@pytest.mark.ig
@pytest.mark.parametrize("gt_graph", gt_test_graphs())
def test_gt2igraph(gt_graph):
    if "node_labels" in gt_graph.vp:
        ig_graph = pyintergraph.gt2igraph(gt_graph, labelname="node_labels")
        nodemap = {v: label for v, label in zip(gt_graph.vertices(), gt_graph.vp["node_labels"])}

        assert list(gt_graph.vp["node_labels"]) == [v["name"] for v in ig_graph.vs()]
        if not gt_graph.is_directed():
            assert set([frozenset((nodemap[e.source()], nodemap[e.target()])) for e in gt_graph.edges()]) == \
                    set([frozenset((nodemap[e.tuple[0]], nodemap[e.tuple[1]])) for e in ig_graph.es()])

        else:
            assert [(nodemap[e.source()], nodemap[e.target()]) for e in gt_graph.edges()] == \
                    [(nodemap[e.tuple[0]], nodemap[e.tuple[1]]) for e in ig_graph.es()]
    else:
        ig_graph = pyintergraph.gt2igraph(gt_graph)

        assert list(gt_graph.get_vertices()) == [v.index for v in ig_graph.vs()]
        if not gt_graph.is_directed():
            assert set([frozenset((e.source(), e.target())) for e in gt_graph.edges()]) == \
                    set([frozenset(e.tuple) for e in ig_graph.es()])

        else:
            assert [(e.source(), e.target()) for e in gt_graph.edges()] == \
                    [e.tuple for e in ig_graph.es()]

@pytest.mark.parametrize("nx_graph", nx_test_graphs())
def test_round_robin_nx(nx_graph):
    graph_tool_graph = pyintergraph.nx2gt(nx_graph, labelname="node_label")

    igraph_graph = pyintergraph.gt2igraph(graph_tool_graph, labelname="node_label")

    reversed_nx_graph = pyintergraph.igraph2nx(igraph_graph)

    assert list(nx_graph.nodes(data=True)) == list(reversed_nx_graph.nodes(data=True))
    assert list(nx_graph.nodes(data=True)) == list(reversed_nx_graph.nodes(data=True))
    assert type(nx_graph) == type(reversed_nx_graph)

@pytest.mark.parametrize("ig_graph", igraph_test_graphs())
def test_round_robin_ig(ig_graph):

    graph_tool_graph = pyintergraph.igraph2gt(ig_graph, labelname="somelabelname")

    nx_graph = pyintergraph.gt2nx(graph_tool_graph, labelname="somelabelname")

    reversed_ig_graph = pyintergraph.nx2igraph(nx_graph)

    assert list(v.index for v in ig_graph.vs()) == list(v.index for v in reversed_ig_graph.vs())
    assert list(e.tuple for e in ig_graph.es()) == list(e.tuple for e in reversed_ig_graph.es())
    assert ig_graph.edge_attributes() == reversed_ig_graph.edge_attributes()
    assert set(ig_graph.vertex_attributes()).add("name") == set(reversed_ig_graph.vertex_attributes()).add("name")
    assert type(ig_graph) == type(reversed_ig_graph)
