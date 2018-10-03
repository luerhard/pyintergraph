from .Graph import InterGraph

def gt2nx(gtG, labelname=None):
    G = InterGraph.from_graph_tool(gtG, labelname=labelname)
    labels = labelname != None
    return G.to_networkX(use_labels=labels)

def nx2gt(nxG, labelname=None):
    G = InterGraph.from_networkX(nxG)
    return G.to_graph_tool(labelname=labelname)

def nx2igraph(nxG):
    G = InterGraph.from_networkX(nxG)
    return G.to_igraph(use_labels=True)

def igraph2nx(iG):
    G = InterGraph.from_igraph(iG)
    return G.to_networkX(use_labels=True)

def gt2igraph(gtG, labelname=None):
    G = InterGraph.from_graph_tool(gtG, labelname=labelname)
    return G.to_igraph(use_labels=True)

def igraph2gt(iG, labelname=None):
    G = InterGraph.from_igraph(iG)
    return G.to_graph_tool(labelname=labelname)