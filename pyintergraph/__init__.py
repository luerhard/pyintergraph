"""Converts Graph Objects between networkX, graph_tools and igraph."""

from .exceptions import PyIntergraphCompatibilityError
from .exceptions import PyIntergraphInferError
from .funcs import gt2igraph
from .funcs import gt2nx
from .funcs import igraph2gt
from .funcs import igraph2nx
from .funcs import nx2gt
from .funcs import nx2igraph
from .inter_graph import InterGraph

USE_LONG_DOUBLE = False

__all__ = [
    "InterGraph",
    "PyIntergraphInferError",
    "PyIntergraphCompatibilityError",
    "nx2gt",
    "nx2igraph",
    "gt2igraph",
    "gt2nx",
    "igraph2gt",
    "igraph2nx",
]
