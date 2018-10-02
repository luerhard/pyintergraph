from .Graph import InterGraph

def gt2nx(gtG, labelname=None):
    G = InterGraph.from_graph_tool(gtG, labelname=labelname)
    labels = labelname != None
    return G.to_networkX(use_labels=labels)