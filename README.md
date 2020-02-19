# pyintergraph

Convert Python-Graph-Objects between networkx, python-igraph and graph-tools. 

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

Graph = pyintergraph.InterGraph.from_networkX(nx_graph)
graph_tool_graph = Graph.to_graph_tool(labelname="node_label")
igraph_graph = Graph.to_igraph()
reversed_nx_graph = Graph.to_networkX()

assert list(nx_graph.nodes(data=True)) == list(reversed_nx_graph.nodes(data=True))
assert list(nx_graph.edges(data=True)) == list(reversed_nx_graph.edges(data=True))
assert type(nx_graph) == type(reversed_nx_graph)
```

# Versions and dependencies
This package ist built and tested with the following configuration:
- python 3.7.6
- networkX 2.4
- igraph 0.8.0
- graph_tool 2.29

## A note on imports and dependencies

Because the installation of python-igraph and graph_tool can be tricky, they are not set as required dependencies for this package. As not everyone has all three packages installed, imports happen just when the two functions of interest are called. That way it is possible to convert networkX-Graphs to igraph-Graphs even when graph_tool is not installed.

## Docker container

If any problems with the installation of python-igraph oder graph_tool arise, the Docker-Container which is used for testing hier can be used: [registry.gitlab.com/luerhard/pyintergraph](https://gitlab.com/luerhard/pyintergraph/container_registry). 

This arch container contains a fully working installation of python 3.7 and three network-libraries that can be converted with this tool. A Dockerfile to rebuild this image can be found in the pacakge-repository on [gitlab.com/luerhard/pyintergraph](https://gitlab.com/luerhard/pyintergraph)
