from collections import defaultdict, abc
import numbers
from .infer import infer_type
from .exceptions import PyIntergraphCompatibilityException


class InterGraph:
    """This defines a interchangeable format that can be read in by the 'from_'-classmethods
    and convert the interchangeable format the package formats with the 'to_'-methods
    """

    def __init__(
        self, nodes, node_labels, node_attributes, edges, edge_attributes, is_directed
    ):
        self.nodes = nodes
        self.node_labels = node_labels
        self.node_attributes = node_attributes

        self.edges = edges
        self.edge_attributes = edge_attributes

        self.is_directed = is_directed
        self.use_labels = True

    @classmethod
    def from_networkx(cls, nxG):
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

        try:
            next(iter(nxG.nodes))
            nodes = list(range(nx.number_of_nodes(nxG)))
            node_labels, node_attributes = zip(*nxG.nodes(data=True))
            node_labels = {node: label for node, label in zip(nodes, node_labels)}
        except StopIteration:
            nodes = []
            node_labels, node_attributes = {}, []

        label_map = {label: node for node, label in node_labels.items()}
        try:
            next(iter(nxG.edges()))
            u_s, v_s, edge_attributes = zip(*nxG.edges(data=True))
        except StopIteration:
            u_s, v_s, edge_attributes = [], [], []

        edges = [(label_map[u], label_map[v]) for u, v in zip(u_s, v_s)]

        return cls(
            nodes, node_labels, node_attributes, edges, edge_attributes, is_directed
        )

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
                attrs = {
                    attr: g.vertex_properties[attr][v]
                    for attr in g.vertex_properties.keys()
                    if not attr == labelname
                }
                yield (v, attrs)

        def create_edges(g):
            for e in g.edges():
                attrs = {
                    attr: g.edge_properties[attr][e]
                    for attr in g.edge_properties.keys()
                    if not attr == labelname
                }
                yield ((e.source(), e.target()), attrs)

        try:
            next(gtG.edges())
            gt_edges, edge_attributes = zip(*create_edges(gtG))
        except StopIteration:
            gt_edges, edge_attributes = [], []

        try:
            next(gtG.vertices())
            gt_nodes, node_attributes = zip(*create_nodes(gtG))
        except StopIteration:
            gt_nodes, node_attributes = [], []

        if len(gt_nodes) == 0:
            return cls([], [], {}, [], [], is_directed)

        # create name-map for nodes
        nodemap = {v: i for v, i in zip(gtG.vertices(), gtG.get_vertices())}
        if labelname:
            node_labels = {
                v: label
                for v, label in zip(
                    gtG.get_vertices(), gtG.vertex_properties[labelname]
                )
            }
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
                    edges.append((u, v))
                else:
                    edges.append((v, u))
            edges = sorted(edges)
        else:
            edges = [(nodemap[u], nodemap[v]) for u, v in gt_edges]

        return cls(
            nodes, node_labels, node_attributes, edges, edge_attributes, is_directed
        )

    @classmethod
    def from_igraph(cls, iG):
        import igraph

        """Converts igraph-Graph to Graph object
        """

        if not isinstance(iG, igraph.Graph):
            raise TypeError("iG must be instance of igraph.Graph() !")

        is_directed = iG.is_directed()

        # check if edges are present
        try:
            edges, edge_attributes = zip(*((e.tuple, e.attributes()) for e in iG.es()))
        except ValueError:
            edges, edge_attributes = [], ()

        # check if nodes are present
        try:
            nodes, node_attributes = zip(*((n.index, n.attributes()) for n in iG.vs()))
        except ValueError:
            nodes, node_attributes = [], ()

        node_labels = {}
        for node, node_attrs in zip(nodes, node_attributes):
            if "name" in node_attrs:
                node_labels[node] = node_attrs["name"]
                del node_attrs["name"]
            else:
                node_labels[node] = node

        return cls(
            list(nodes),
            node_labels,
            node_attributes,
            list(edges),
            edge_attributes,
            is_directed,
        )

    def to_networkx(self):
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

        # is multi?
        is_multigraph = len(self.edges) > len(set(self.edges))

        # select appropriate networkX-Graph-Type
        if self.is_directed and not is_multigraph:
            nxG = nx.DiGraph()
        elif not self.is_directed and not is_multigraph:
            nxG = nx.Graph()
        elif not self.is_directed and is_multigraph:
            nxG = nx.MultiGraph()
        else:
            nxG = nx.MultiDiGraph()

        nxG.add_nodes_from(
            zip((self.node_labels[n] for n in self.nodes), self.node_attributes)
        )

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

        if len(self.nodes) == 0:
            return gtG

        attrs = {}
        node_type = infer_type(self.node_labels.values(), as_vector=False)

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
                # Single Type assertion
                node_property_type_assertion[key].add(type(val))
                if len(node_property_type_assertion[key]) > 1:
                    raise Exception(
                        f"Type not equal for all nodes on Node-Attribute {key}, \
                        types found: {node_property_type_assertion[key]}"
                    )

                if key not in attrs:
                    as_vector = isinstance(val, abc.Iterable) and not isinstance(
                        val, str
                    )
                    attrs[key] = gtG.new_vertex_property(
                        infer_type(val, as_vector=as_vector)
                    )

                attrs[key][v] = val

        for attr_name, attr_val in attrs.items():
            gtG.vertex_properties[attr_name] = attr_val

        attrs = {}
        edge_property_assertion = defaultdict(set)
        for e, data in zip(self.edges, self.edge_attributes):
            u, v = e
            edge = gtG.add_edge(nodes[u], nodes[v])
            for key, val in data.items():
                # Single Type assertion
                edge_property_assertion[key].add(type(val))
                if len(edge_property_assertion[key]) > 1:
                    raise Exception(
                        f"Type not equal for all edges on Edge-Attribute {key}, \
                        types found: {edge_property_assertion[key]}"
                    )

                if key not in attrs:
                    as_vector = isinstance(val, abc.Iterable) and not isinstance(
                        val, str
                    )
                    attrs[key] = gtG.new_edge_property(
                        infer_type(val, as_vector=as_vector)
                    )

                attrs[key][edge] = val

        for attr_key, attr_val in attrs.items():
            gtG.edge_properties[attr_key] = attr_val

        return gtG

    def to_igraph(self):
        import igraph as ig

        iG = ig.Graph(directed=self.is_directed)

        use_labels = True

        try:
            label_type = type(next(iter(self.node_labels)))
        except StopIteration:
            return iG

        if issubclass(label_type, numbers.Number):
            use_labels = False

        for i, (node, attr) in enumerate(zip(self.nodes, self.node_attributes)):
            if use_labels is True:
                iG.add_vertex(self.node_labels[node], **attr)
            else:
                if "name" in attr:
                    raise PyIntergraphCompatibilityException(
                        "Your network seems to have 'name' as a node attribute. "
                        "This is a reserved keyword for node labels in python-igraph. "
                        "You cannot use that !"
                    )
                iG.add_vertex()
                iG.vs[i].update_attributes(name=self.node_labels[node], **attr)

        for edge, attr in zip(self.edges, self.edge_attributes):
            u, v = edge
            # Handle for weird 'name' or 'Vertex-ID' input in igraph
            if use_labels is True:
                u = self.node_labels[u]
                v = self.node_labels[v]

            iG.add_edge(u, v, **attr)

        return iG
