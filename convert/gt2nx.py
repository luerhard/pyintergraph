from .Graph import Graph

def gt2nx(gtG, labelname=None):
    G = Graph.from_graph_tool(gtG, labelname=labelname)
    labels = labelname != None
    return G.to_networkX(use_labels=labels)