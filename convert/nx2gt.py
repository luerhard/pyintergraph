from .Graph import InterGraph

def nx2gt(nxG, labelname=None):
    G = InterGraph.from_networkX(nxG)
    return G.to_graph_tool(labelname=labelname)