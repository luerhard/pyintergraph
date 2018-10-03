from collections import defaultdict

from .infer import infer_type

class InterGraph:
    """This defines a interchangeable format that can be read in by the 'from_'-classmethods
        and convert the interchangeable format the package formats with the 'to_'-methods
    """
    def __init__(self, nodes, node_labels, node_attributes, edges, edge_attributes, is_directed):
        self.nodes = nodes
        self.node_labels = node_labels
        self.node_attributes = node_attributes

        self.edges = edges
        self.edge_attributes = edge_attributes

        self.is_directed = is_directed

    @classmethod
    def from_networkX(cls, nxG):
        """Converts networkX Graph to Graph object

        :params:
            nxG:networkX-Graph
        :returns:
            Graph object
        """
        
        is_directed = nxG.is_directed()

        node_labels, node_attributes = list(zip(*nxG.nodes(data=True)))
        nodes, _ = list(zip(*enumerate(node_labels)))

        u, v, edge_attributes = zip(*nxG.edges(data=True))
        edges = list(zip(u,v))

        return cls(nodes, node_labels, node_attributes, edges, edge_attributes, is_directed)

    @classmethod
    def from_graph_tool(cls, gtG, labelname=None):
        """Converts graph-tool Object to Graph

        :params:
            gtG:graph-tool Graph object
            labelname:None or vertex_attribute
                if None node labels will be set equal to vertex-indices.
                otherwise a vertex-attribute, that contains the node labels can be set.
        :returns:
            Graph object
        """

        is_directed = gtG.is_directed()

        def create_nodes(g):
            for v in g.vertices():
                attrs = {attr: g.vertex_properties[attr][v] \
                    for attr in g.vertex_properties.keys() \
                    if not attr == labelname}
                yield (v, attrs)

        def create_edges(g):
            for e in g.edges():
                attrs = {attr: g.edge_properties[attr][e] \
                    for attr in g.edge_properties.keys() \
                    if not attr == labelname}
                yield ((e.source(), e.target()), attrs)

        gt_edges, edge_attributes = zip(*list(create_edges(gtG)))
        gt_nodes, node_attributes = zip(*list(create_nodes(gtG)))

        #create name-map for nodes
        if labelname:
            nodemap = {v: label for v, label in zip(gtG.vertices(), gtG.vertex_properties[labelname])}
            node_labels = [nodemap[node] for node in gt_nodes]
            nodes = [gtG.vertex(i, use_index=False) for i in gt_nodes]
        else:
            nodemap = {gtG.vertex(i, use_index=False): i for i in gtG.get_vertices()}
            node_labels = [nodemap[node] for node in gt_nodes]
            nodes = node_labels

        edges = [(nodemap[u], nodemap[v]) for u, v in gt_edges]

        return cls(nodes, node_labels, node_attributes, edges, edge_attributes, is_directed)

    
    @classmethod
    def from_igraph(cls, iG):
        """Converts igraph-Graph to Graph object
        """
        is_directed = iG.is_directed()
        edges, edge_attributes = list(zip(*((e.tuple, e.attributes()) for e in iG.es())))
        nodes, node_attributes = list(zip(*((n.index, n.attributes()) for n in iG.vs())))

        node_labels = []
        for node in node_attributes:
            node_labels.append(node["name"])
            del node["name"] 
        
        return cls(nodes, node_labels, node_attributes, edges, edge_attributes, is_directed)

    def to_networkX(self, use_labels=True):
        """
        Converts Graph object to networkX Graph.

        :params:
            use_labels:bool, defaults to true
                choose whether to use labels or indices as names for the nodes.
                if no specific labels were read in, these to are equal.
               
        :returns:
            networkX Graph, DiGraph, MultiGraph or MultiDiGraph
        """
        import networkx as nx
                
        #is multi?
        is_multigraph = len(self.edges) > len(set(self.edges))
        
        #select appropriate networkX-Graph-Type
        if self.is_directed and not is_multigraph:
            nxG = nx.DiGraph()
        elif not self.is_directed and not is_multigraph:
            nxG = nx.Graph()
        elif not self.is_directed and is_multigraph:
            nxG = nx.MultiGraph()
        else:
            nxG = nx.MultiDiGraph()

        if use_labels:
            nodes = self.node_labels
        else:
            nodes = self.nodes

        nxG.add_nodes_from(zip(nodes, self.node_attributes))
        nxG.add_edges_from(self.edges)
        for edge, edge_attr in zip(self.edges, self.edge_attributes):
            u, v = edge
            nxG.add_edge(u,v,**edge_attr)
                        
        return nxG

    def to_graph_tool(self, labelname=None):
        """Converts Graph object to graph-tool Graph.

        :params:
            labelname: name for vertex_attribute None, defaults to None.
                if node labels should be kept as vertex attribute,
                the name for the vertex attribute can be specified this way.
        """
        import graph_tool.all as gt

        gtG = gt.Graph(directed=self.is_directed)

        attrs = {}
        node_type = {type(n) for n in self.edges}
        if len(node_type) == 1:
            node_type = infer_type(self.nodes[0])
        else:
            node_type = "string"
        
        if labelname:
            attrs[labelname] = gtG.new_vertex_property(node_type)

        nodes = {}
        node_property_type_assertion = defaultdict(set)

        for nx_node, data in zip(self.node_labels, self.node_attributes):

            v = gtG.add_vertex()
            if labelname:
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
        for e, data in zip(self.edges, self.edge_attributes):
            u, v = e
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

    def to_igraph(self, use_labels=True):
        import igraph as ig

        iG = ig.Graph(directed=self.is_directed)

        if use_labels:
            nodemap = {node: node_label for node, node_label in zip(self.nodes, self.node_labels)}

            for node, attr in zip(self.nodes, self.node_attributes):
                iG.add_vertex(nodemap[node], **attr)
            
            for edge, attr in zip(self.edges, self.edge_attributes):
                u,v = edge
                iG.add_edge(nodemap[u], nodemap[v], **attr)
        else:
            for node, attr in zip(self.nodes, self.node_attributes):
                iG.add_vertex(node, **attr)
            
            for edge, attr in zip(self.edges, self.edge_attributes):
                u, v = edge
                iG.add_edge(u, v, **attr)

        return iG
