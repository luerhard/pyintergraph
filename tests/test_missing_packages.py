import sys

import pytest

from .testdata.gtdata import gt_test_graphs
from .testdata.igraphdata import igraph_test_graphs
from .testdata.networkxdata import nx_test_graphs

class MissingTemplate:
    module = None

    @classmethod
    def setup_class(cls):
        cls._temp_module = None
        if sys.modules.get(cls.module):
            cls._temp_module = sys.modules[cls.module]
        sys.modules[cls.module] = None

    @classmethod
    def teardown_class(cls):
        if cls._temp_module:
            sys.modules[cls.module] = cls._temp_module
        else:
            del sys.modules[cls.module]


@pytest.mark.missing_gt()
class TestMissingGT(MissingTemplate):
    module = "graph_tool"

    def test_missing(self):
        flag = False
        try:
            import graph_tool
        except ImportError:
            flag = True

        assert flag is True

    @pytest.mark.parametrize("graph", igraph_test_graphs())
    def test_raises_igraph_to_gt(self, graph):
        import pyintergraph

        with pytest.raises(ImportError, match="Could not import graph_tool."):
            _ = pyintergraph.igraph2gt(graph)

    @pytest.mark.parametrize("graph", nx_test_graphs())
    def test_nx_to_igraph(self, graph):
        import pyintergraph

        _ = pyintergraph.nx2igraph(graph)
        assert True


class TestMissingNetworkx(MissingTemplate):
    module = "networkx"

    def test_missing(self):
        flag = False
        try:
            import networkx
        except ImportError:
            flag = True

        assert flag is True

    @pytest.mark.parametrize("graph", igraph_test_graphs())
    def test_igraph_to_gt(self, graph):
        import pyintergraph

        _ = pyintergraph.igraph2gt(graph)
        assert True

    @pytest.mark.parametrize("graph", gt_test_graphs())
    def test_gt_to_igraph(self, graph):
        import pyintergraph

        _ = pyintergraph.gt2igraph(graph)
        assert True

    @pytest.mark.parametrize("graph", gt_test_graphs())
    def test_raises_gt_to_nx(self, graph):
        import pyintergraph

        with pytest.raises(ImportError, match="Could not import networkx."):
            _ = pyintergraph.gt2nx(graph)


class TestMissingIgraph(MissingTemplate):
    module = "igraph"

    def test_missing(self):
        flag = False
        try:
            import igraph
        except ImportError:
            flag = True

        assert flag is True

    @pytest.mark.parametrize("graph", nx_test_graphs())
    def test_nx_to_gt(self, graph):
        import pyintergraph

        _ = pyintergraph.nx2gt(graph)
        assert True

    @pytest.mark.parametrize("graph", gt_test_graphs())
    def test_raises_gt_to_igraph(self, graph):
        import pyintergraph

        with pytest.raises(ImportError, match="Could not import igraph."):
            _ = pyintergraph.gt2igraph(graph)
