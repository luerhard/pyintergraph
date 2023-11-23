# pyintergraph

Convert Python-Graph-Objects between networkx, python-igraph and graph-tool. 

# Installation 
This package can be installed via:
```
pip install pyintergraph
```
For the note on imports and dependencies, see the section at the bottom of the page. 

# Usage

```python
import networkx as nx
import pyintergraph

nx_graph = nx.karate_club_graph()

graph_tool_graph = pyintergraph.nx2gt(nx_graph, labelname="node_label")
igraph_graph = pyintergraph.gt2igraph(graph_tool_graph, labelname="node_label")
reversed_nx_graph = pyintergraph.igraph2nx(igraph_graph)

# or

Graph = pyintergraph.InterGraph.from_networkx(nx_graph)
graph_tool_graph = Graph.to_graph_tool(labelname="node_label")
igraph_graph = Graph.to_igraph()
reversed_nx_graph = Graph.to_networkx()

assert list(nx_graph.nodes(data=True)) == list(reversed_nx_graph.nodes(data=True))
assert list(nx_graph.edges(data=True)) == list(reversed_nx_graph.edges(data=True))
assert type(nx_graph) == type(reversed_nx_graph)
```

## A note on imports and dependencies

Because the installation of python-igraph and graph_tool can be tricky, they are not set as required dependencies for this package. As not everyone has all three packages installed, imports happen just when the two functions of interest are called. That way it is possible to convert networkX-Graphs to igraph-Graphs even when graph_tool is not installed.
