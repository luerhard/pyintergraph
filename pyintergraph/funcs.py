from .Graph import InterGraph


def nx2gt(nxG, labelname=None):
    G = InterGraph.from_networkx(nxG)
    return G.to_graph_tool(labelname=labelname)


def nx2igraph(nxG):
    G = InterGraph.from_networkx(nxG)
    return G.to_igraph()


def gt2nx(gtG, labelname=None):
    G = InterGraph.from_graph_tool(gtG, labelname=labelname)
    return G.to_networkx()


def gt2igraph(gtG, labelname=None):
    G = InterGraph.from_graph_tool(gtG, labelname=labelname)
    return G.to_igraph()


def igraph2nx(iG):
    G = InterGraph.from_igraph(iG)
    return G.to_networkx()


def igraph2gt(iG, labelname=None):
    G = InterGraph.from_igraph(iG)
    return G.to_graph_tool(labelname=labelname)
