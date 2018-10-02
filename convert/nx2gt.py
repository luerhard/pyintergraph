from .Graph import Graph

def nx2gt(nxG, labelname="label"):
    G = Graph.from_networkX(nxG)
    return G.to_graph_tool(labelname=labelname)