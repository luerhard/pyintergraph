# pyintergraph
Exchange Python-Graph-Objects between networkx, igraph and graph-tools

# Usage
import the Repository-folder as a package:

```
import networkx as nx
from pyintergraph import InterGraph, nx2gt, gt2nx

nx_graph = nx.karate_club_graph()
graph_tool_graph = nx2gt(nx_graph, label_name="node_label)
reversed_nx_graph = gt2nx(graph_tool_graph, use_labels=True)

# or

Graph = InterGraph.from_networkX(nx_graph)
graph_tool_graph = Graph.to_graph_tool(labelname="node_label")
reversed_nx_graph = Graph.to_networkX(use_labels=True)
```
