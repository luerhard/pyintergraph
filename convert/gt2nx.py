import networkx as nx
import graph_tool.all as gt

def gt2nx(gtG, labelname=None):
    """
    Converts graph-tool Graph object to networkX Graph.

    :params:
        gtG: graph-tool Graph
            The Graph that is to be converted.
        labelname: property-key, optional
            if given, the created nodes in the new Graph will be named according to this vertex_property,
            otherwise they will be named according to the vertex-index.

    :returns:
        networkX Graph
    """
    
    #infer type
    # is directed?
    is_directed = gtG.is_directed()
    
    #is multi?
    is_multigraph = sum(1 for e in gtG.edges()) > len({(e.source(), e.target()) for e in gtG.edges()})
    
    #select appropriate networkX-Graph-Type
    if is_directed and not is_multigraph:
        nxG = nx.DiGraph()
    elif not is_directed and not is_multigraph:
        nxG = nx.Graph()
    elif not is_directed and is_multigraph:
        nxG = nx.MultiGraph()
    else:
        nxG = nx.MultiDiGraph()
    
    #create name-map for nodes
    if labelname:
        nodes = {v: label for v, label in zip(gtG.vertices(), gtG.vertex_properties[labelname])}
    else:
        nodes = {gtG.vertex(i, use_index=False): i for i in gtG.get_vertices()}
    
    #add nodes
    def generate_nodes(g):
        for v in g.vertices():
            attrs = {attr: g.vertex_properties[attr][v] for attr in g.vertex_properties.keys() if not attr == labelname}
            yield (v, attrs)
    
    nxG.add_nodes_from((nodes[v], attr) for v, attr in generate_nodes(gtG))
    
    #add edges
    def generate_edges(g):
        for e in g.edges():
            attrs = {attr: g.edge_properties[attr][e] for attr in g.edge_properties.keys()}
            yield((e, attrs))
    
    nxG.add_edges_from((nodes[e.source()], nodes[e.target()], attr) for e, attr in generate_edges(gtG))
        
        
    return nxG
