from collections import defaultdict

import networkx as nx 
import graph_tool.all as gt

from .infer import infer_type

def nx2gt(nxG, labelname="label"):
    """
    Converts networkx-graph to graph_tool graph
    
    :params:
        G : networkx graph object
            The Graph that is to be converted
        labelname: hashable, optional
            The name of the vertex_property that the nodelabels should be stored in.
            Defaults to 'label'.

    :returns:
        tuple(graph, node_labels)
    """
    assert isinstance(nxG, nx.Graph), "G not in implemented networkX-Graph type!"

    directed = nx.is_directed(nxG)
    gtG = gt.Graph(directed=directed)

    attrs = {}
    node_type = {type(n) for n in nxG}
    if len(node_type) == 1:
        node_type = infer_type(next(iter(nxG.nodes())))
    else:
        node_type = "string"
    attrs[labelname] = gtG.new_vertex_property(node_type)

    nodes = {}
    node_property_type_assertion = defaultdict(set)

    for nx_node, data in nxG.nodes(data=True):

        v = gtG.add_vertex()
        attrs[labelname][v] = nx_node
        nodes[nx_node] = v

        for key, val in data.items():

            #Single Type assertion
            node_property_type_assertion[key].add(type(val))
            if len(node_property_type_assertion[key]) > 1:
                raise Exception(f"Type not equal for all nodes on Node-Attribute {key}, \
                    types found: {node_property_type_assertion[key]}")

            if key not in attrs:
                attrs[key] = gtG.new_vertex_property(infer_type(val))
            
            attrs[key][v] = val
            
    for attr_name, attr_val in attrs.items():
        gtG.vertex_properties[attr_name] = attr_val        

    attrs = {}
    edge_property_assertion = defaultdict(set)
    for u,v, data in nxG.edges(data=True):

        edge = gtG.add_edge(nodes[u], nodes[v])
        for key, val in data.items():
            
            #Single Type assertion
            edge_property_assertion[key].add(type(val))
            if len(edge_property_assertion[key]) > 1:
                raise Exception(f"Type not equal for all edges on Edge-Attribute {key}, \
                    types found: {edge_property_assertion[key]}")
            
            if key not in attrs:
                attrs[key] = gtG.new_edge_property(infer_type(val))
            
            attrs[key][edge] = val

    for attr_key, attr_val in attrs.items():
        gtG.edge_properties[attr_key] = attr_val 

    return gtG



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
    