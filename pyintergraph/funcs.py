"""Shorthand function that allow a quick conversion.

They all use InterGraph under the hood.
"""

from .inter_graph import InterGraph

def nx2gt(nx_graph, labelname=None):
    """Converts a networkX graph to a graph_tool graph.

    Args:
        nx_graph (:class:`networkx.Graph`): The graph to be converted.
        labelname (str, optional): graph_tool forces integers as node ids. If the node labels
            should be kept, labelname can be set to a name for the new node attribute, the labels
            are to be stored in. Defaults to None (node labels are not kept).

    Returns:
        :class:`graph_tool.Graph`: Converted graph_tool graph.
    """
    G = InterGraph.from_networkx(nx_graph)
    return G.to_graph_tool(labelname=labelname)


def nx2igraph(nx_graph):
    """Converts a networkX graph to a graph_tool graph.

    Args:
        nx_graph (:class:`networkx.Graph`): Graph that should be converted to igraph.

    Returns:
        :class:`igraph.Graph`: Converted igraph graph.
    """
    G = InterGraph.from_networkx(nx_graph)
    return G.to_igraph()


def gt2nx(gt_graph, labelname=None):
    """Converts a graph_tool graph to a networkx graph.

    Args:
        gt_graph (:class:`graph_tool.Graph`): graph_tool graph to be converted.
        labelname (str, optional): graph_tool allows only integer ids for nodes. If node
            labels are stored in a node attribute, it can be set here to extract them for the
            igraph version. Defaults to None (No special handling for node labels).

    Returns:
        :class:`graph_tool.Graph`: Converted graph_tool graph.
    """
    G = InterGraph.from_graph_tool(gt_graph, labelname=labelname)
    return G.to_networkx()


def gt2igraph(gt_graph, labelname=None):
    """Converts a graph_tool graph to an igraph graph.

    Args:
        gt_graph (:class:`graph_tool.Graph`): graph_tool graph to be converted
        labelname (str, optional): graph_tool allows only integer ids for nodes. If node
            labels are stored in a node attribute, it can be set here to extract them for the
            igraph version. Defaults to None (No special handling for node labels).

    Returns:
        :class:`igraph.Graph`: Converted igraph graph.
    """
    G = InterGraph.from_graph_tool(gt_graph, labelname=labelname)
    return G.to_igraph()


def igraph2nx(igraph_graph):
    """Converts an igraph graph to a networkX graph.

    Args:
        igraph_graph (:class:`igraph.Graph`): igraph graph that should be converted to networkX.

    Returns:
         :class:`networkx.Graph`: Converted networkX graph.
    """
    G = InterGraph.from_igraph(igraph_graph)
    return G.to_networkx()


def igraph2gt(igraph_graph, labelname=None):
    """Converts an igraph graph to a graph_tool graph.

    Args:
        igraph_graph (:class:`igraph.Graph`): igraph graph that should be converted to graph_tool.
        labelname (str, optional): graph_tool forces integers as node ids. If the node labels
            should be kept, labelname can be set to a name for the new node attribute, the labels
            are to be stored in. Defaults to None (node labels are not kept).

    Returns:
        :class:`graph_tool.Graph`: Converted graph_tool graph.
    """
    G = InterGraph.from_igraph(igraph_graph)
    return G.to_graph_tool(labelname=labelname)
