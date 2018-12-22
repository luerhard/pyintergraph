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
        import networkx as nx

        if not isinstance(nxG, nx.Graph):
            raise TypeError("nxG must be instance of nx.Graph oder subclasses thereof!")
        
        is_directed = nxG.is_directed()

        nodes = list(range(nx.number_of_nodes(nxG)))
        node_labels, node_attributes = zip(*nxG.nodes(data=True))
        node_labels = {node: label for node, label in zip(nodes, node_labels)}

        label_map = {label: node for node, label in node_labels.items()}
        u_s, v_s, edge_attributes = zip(*nxG.edges(data=True))
        edges = [(label_map[u], label_map[v]) for u, v in zip(u_s, v_s)]

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
        from graph_tool import Graph

        if not isinstance(gtG, Graph):
            raise TypeError("gtG must be an instance of graph_tool.Graph() !")

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

        gt_edges, edge_attributes = zip(*create_edges(gtG))
        gt_nodes, node_attributes = zip(*create_nodes(gtG))

        #create name-map for nodes
        nodemap = {v: i for v, i in zip(gtG.vertices(), gtG.get_vertices())}
        if labelname:
            node_labels = {v: label for v, label in \
                zip(gtG.get_vertices(), gtG.vertex_properties[labelname])}
            nodes = list(node_labels.keys())
        else:
            node_labels = {i: i for i in gtG.get_vertices()}
            nodes = list(node_labels.keys())

        if not is_directed:
            edges = []
            for u, v in gt_edges:
                u = nodemap[u]
                v = nodemap[v]
                if node_labels[u] < node_labels[v]:
                    edges.append((u,v))
                else:
                    edges.append((v,u))
            edges = sorted(edges)
        else:
            edges = [(nodemap[u], nodemap[v]) for u, v in gt_edges]
        
        return cls(nodes, node_labels, node_attributes, edges, edge_attributes, is_directed)

    
    @classmethod
    def from_igraph(cls, iG):
        import igraph
        """Converts igraph-Graph to Graph object
        """

        if not isinstance(iG, igraph.Graph):
            raise TypeError("iG must be instance of igraph.Graph() !")

        is_directed = iG.is_directed()
        edges, edge_attributes = zip(*((e.tuple, e.attributes()) for e in iG.es()))
        nodes, node_attributes = zip(*((n.index, n.attributes()) for n in iG.vs()))

        node_labels = {}
        for node, node_attrs in zip(nodes, node_attributes):
            if "name" in node_attrs:
                node_labels[node] = node_attrs["name"]
                del node_attrs["name"]
            else:
                node_labels[node] = node 

        
        return cls(list(nodes), node_labels, node_attributes, list(edges), edge_attributes, is_directed)

    def to_networkX(self):
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

        nxG.add_nodes_from(zip((self.node_labels[n] for n in self.nodes), self.node_attributes))

        for edge, edge_attr in zip(self.edges, self.edge_attributes):
            u, v = edge
            nxG.add_edge(self.node_labels[u], self.node_labels[v], **edge_attr)
                        
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
        node_type = infer_type(self.node_labels.values())
        
        if labelname:
            attrs[labelname] = gtG.new_vertex_property(node_type)

        nodes = {}
        node_property_type_assertion = defaultdict(set)

        for nx_node, data in zip(self.nodes, self.node_attributes):

            v = gtG.add_vertex()
            if labelname:
                attrs[labelname][v] = self.node_labels[nx_node]
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

    def to_igraph(self):
        import igraph as ig

        iG = ig.Graph(directed=self.is_directed)

         
        for node, attr in zip(self.nodes, self.node_attributes):
            iG.add_vertex(self.node_labels[node], **attr)
        
        for edge, attr in zip(self.edges, self.edge_attributes):
            u,v = edge
            iG.add_edge(self.node_labels[u], self.node_labels[v], **attr)
       
        return iG
