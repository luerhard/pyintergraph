import pytest

import pyintergraph

from .Data import gt_graph_list, nx_graph_list, ig_graph_list

#Tests
@pytest.mark.parametrize("nx_graph", nx_graph_list)
def test_nx2igraph_with_labels(nx_graph):
    ig_graph = pyintergraph.nx2igraph(nx_graph)

    assert list(nx_graph.nodes()) == [v["name"] for v in ig_graph.vs()]
    assert [e for e in nx_graph.edges()] == [e.tuple for e in ig_graph.es()]

@pytest.mark.parametrize("nx_graph", nx_graph_list)
def test_nx2gt_with_labels(nx_graph):
    gt_graph = pyintergraph.nx2gt(nx_graph, labelname="node_label")

    assert list(gt_graph.vp["node_label"]) == list(nx_graph.nodes())
    assert [(e.source(), e.target()) for e in gt_graph.edges()] == list(nx_graph.edges())

@pytest.mark.parametrize("ig_graph", ig_graph_list)
def test_igraph2nx_with_labels(ig_graph):
    nx_graph = pyintergraph.igraph2nx(ig_graph)

    assert list(nx_graph.nodes()) == [v["name"] for v in ig_graph.vs()]
    assert [e for e in nx_graph.edges()] == [e.tuple for e in ig_graph.es()]

@pytest.mark.parametrize("ig_graph", ig_graph_list)
def test_igraph2gt_with_labels(ig_graph):
    gt_graph = pyintergraph.igraph2gt(ig_graph, labelname="node_label")

    assert [v["name"] for v in ig_graph.vs()] == list(gt_graph.vp["node_label"])
    assert [e.tuple for e in ig_graph.es()] == [(e.source(), e.target()) for e in gt_graph.edges()]

@pytest.mark.parametrize("gt_graph", gt_graph_list)
def test_gt2nx_with_labels(gt_graph):
    nx_graph = pyintergraph.gt2nx(gt_graph, labelname="node_labels")
    nodemap = {v: label for v, label in zip(gt_graph.vertices(), gt_graph.vp["node_labels"])}

    assert list(gt_graph.vp["node_labels"]) == list(nx_graph.nodes())
    assert [(nodemap[e.source()], nodemap[e.target()]) for e in gt_graph.edges()] == list(nx_graph.edges())

@pytest.mark.parametrize("gt_graph", gt_graph_list)
def test_gt2igraph_with_labels(gt_graph):
    ig_graph = pyintergraph.gt2igraph(gt_graph, labelname="node_labels", use_labels=True)
    nodemap = {v: label for v, label in zip(gt_graph.vertices(), gt_graph.vp["node_labels"])}

    assert list(gt_graph.vp["node_labels"]) == [v["name"] for v in ig_graph.vs()]

    assert [(nodemap[e.source()], nodemap[e.target()]) for e in gt_graph.edges()] == \
            [(nodemap[e.tuple[0]], nodemap[e.tuple[1]]) for e in ig_graph.es()]
