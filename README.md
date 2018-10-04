# pyintergraph
Exchange Python-Graph-Objects between networkx, igraph and graph-tools

# Usage
import the Repository-folder as a package:

```
import networkx as nx
import pyintergraph

import pyintergraph

nx_graph = nx.karate_club_graph()

graph_tool_graph = pyintergraph.nx2gt(nx_graph, labelname="node_label")

igraph_graph = pyintergraph.gt2igraph(graph_tool_graph, labelname="node_label")

reversed_nx_graph = pyintergraph.igraph2nx(igraph_graph)

list(nx_graph.nodes(data=True)) == list(reversed_nx_graph.nodes(data=True))
-> True
list(nx_graph.nodes(data=True)) == list(reversed_nx_graph.nodes(data=True))
-> True
type(nx_graph) == type(reversed_nx_graph)
-> True

# or

Graph = InterGraph.from_networkX(nx_graph)

graph_tool_graph = Graph.to_graph_tool(labelname="node_label")

igraph_graph = Graph.to_igraph()

reversed_nx_graph = Graph.to_networkX()

```

# A note on imports

As not everyone has all three packages installed, imports happen just when the two functions of interest are called. So it is possible to convert networkX-Graphs to igraph-Graphs even when graph_tool is not installed.
