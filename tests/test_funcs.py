import pytest

import pyintergraph

from .testdata.networkxdata import nx_test_graphs
from .testdata.igraphdata import igraph_test_graphs
from .testdata.gtdata import gt_test_graphs

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
    nodemap = {v: label for v, label in zip(gt_graph.vertices(), gt_graph.vp["node_label"])}

    assert list(gt_graph.vp["node_label"]) == list(nx_graph.nodes())
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

    if hasattr(ig_graph.vs, "name"):
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

    if hasattr(ig_graph.vs, "name"):
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
