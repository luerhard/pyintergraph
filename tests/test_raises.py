import pytest

import pyintergraph

@pytest.fixture
def wrong_input():
    return "MyGraph"

@pytest.mark.ig
def test_igraph2nx_raises(wrong_input):
    with pytest.raises(TypeError):
        g = pyintergraph.igraph2nx(wrong_input)

def test_igraph2gt_raises(wrong_input):
    with pytest.raises(TypeError):
        g = pyintergraph.igraph2gt(wrong_input)

@pytest.mark.gt
def test_gt2nx_raises(wrong_input):
    with pytest.raises(TypeError):
        g = pyintergraph.gt2nx(wrong_input)

def test_gt2igraph_raises(wrong_input):
    with pytest.raises(TypeError):
        g = pyintergraph.gt2igraph(wrong_input)

@pytest.mark.nx
def test_nx2gt_raises(wrong_input):
    with pytest.raises(TypeError):
        g = pyintergraph.nx2gt(wrong_input)

def test_nx2igraph_raises(wrong_input):
    with pytest.raises(TypeError):
        g = pyintergraph.nx2igraph(wrong_input)