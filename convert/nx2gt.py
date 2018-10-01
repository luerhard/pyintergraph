from collections import defaultdict

import networkx as nx 
import graph_tool.all as gt

from .infer import infer_type

def nx2gt(G):
    """
    Converts networkx-graph to graph_tool graph
    
    :params:
        G : networkx graph object

    :returns:
        tuple(graph, node_labels)
    """
    assert isinstance(G, (nx.Graph,nx.DiGraph)), "G not in implemented networkX-Graph type!"

    directed = nx.is_directed(G)
    B = gt.Graph(directed=directed)


    attrs = {}
    attrs["name"] = B.new_vertex_property("string")

    nodes = {}
    node_property_type_assertion = defaultdict(set)

    for nx_node, data in G.nodes(data=True):

        v = B.add_vertex()
        attrs["name"][v] = nx_node
        nodes[nx_node] = v

        for key, val in data.items():

            #Single Type assertion
            node_property_type_assertion[key].add(type(val))
            if len(node_property_type_assertion[key]) > 1:
                raise Exception(f"Type not equal for all nodes on Node-Attribute {key}, \
                    types found: {node_property_type_assertion[key]}")

            if key not in attrs:
                attrs[key] = B.new_vertex_property(infer_type(val))
            
            attrs[key][v] = val
            
    for attr_name, attr_val in attrs.items():
        B.vertex_properties[attr_name] = attr_val        

    attrs = {}
    edge_property_assertion = defaultdict(set)
    for u,v, data in G.edges(data=True):

        edge = B.add_edge(nodes[u], nodes[v])
        for key, val in data.items():
            
            #Single Type assertion
            edge_property_assertion[key].add(type(val))
            if len(edge_property_assertion[key]) > 1:
                raise Exception(f"Type not equal for all edges on Edge-Attribute {key}, \
                    types found: {edge_property_assertion[key]}")
            
            if key not in attrs:
                attrs[key] = B.new_edge_property(infer_type(val))
            
            attrs[key][edge] = val

    for attr_key, attr_val in attrs.items():
        B.edge_properties[attr_key] = attr_val 


    print(f"Number of Nodes in new Graph: {sum(1 for _ in B.vertices())}")
    print(f" -> in old Graph {len(G.nodes())}")

    return B



if __name__ == "__main__":
    g = nx.DiGraph()
    g.add_nodes_from([
        ("me", {"t": "1"}),
        (20,{"t": "1"}),
        ("3",{"t": "2"}),
        (4)
        ])
    g.add_edges_from([
        ("me",20, {"weight": 0.1}), 
        (20,"3"), 
        (20, 4)
        ])
    g = nx2gt(g)
    print([n.title() for n in g.vertex_properties["name"]])
    print([n.title() for n in g.vertex_properties["t"]])
    print([n.real for n in g.edge_properties["weight"]])
    print(g.list_properties())
    gt.graph_draw(g, vertex_text=g.vertex_properties["name"], vertex_font_size=18, output_size=(200, 200), output="graph.png")
    print(gt.betweenness(g)[0].get_array())