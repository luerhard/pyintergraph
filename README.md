# pyintergraph
Exchange Python-Graph-Objects between networkx, igraph and graph-tools

# Usage
import the Repository-folder as a package:

```
import networkx as nx
import pyintergraph as pyint

nx_graph = nx.karate_club_graph()

graph_tool_graph = pyint.nx2gt(nx_graph, label_name="node_label)
reversed_nx_graph = pyint.gt2nx(graph_tool_graph, use_labels=True)

igraph_graph = pyint.nx2igraph(nx_graph)

# or

Graph = InterGraph.from_networkX(nx_graph)
graph_tool_graph = Graph.to_graph_tool(labelname="node_label")
reversed_nx_graph = Graph.to_networkX(use_labels=True)
igraph_graph = Graph.to_igraph()
```
