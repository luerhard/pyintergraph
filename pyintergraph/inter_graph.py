"""Base class that does all the conversions."""

from collections import abc
from collections import defaultdict
from collections.abc import Iterable
import numbers
from typing import Self

from .exceptions import PyIntergraphCompatibilityError
from .infer import infer_type


class InterGraph:
    """This defines a interchangeable format.

    It can be read in by the `from_`-classmethods and convert the interchangeable format the
    package formats with the `to_`-methods
    """

    def __init__(  # noqa: D107
        self,
        nodes: Iterable,
        node_labels: dict,
        node_attributes: Iterable,
        edges: Iterable[tuple],
        edge_attributes: Iterable,
        is_directed: bool,
    ):
        self.nodes = nodes
        self.node_labels = node_labels
        self.node_attributes = node_attributes

        self.edges = edges
        self.edge_attributes = edge_attributes

        self.is_directed = is_directed
        self.use_labels = True

    @classmethod
    def from_networkx(cls, nx_graph) -> Self:
        """Converts networkX Graph to InterGraphGraph object.

        Args:
            nx_graph (:class:`networkx.Graph`): The Graph to convert to Intergraph
        Returns:
            An InterGraph object
        """
        try:
            import networkx as nx
        except (ModuleNotFoundError, ImportError) as e:
            msg = "Could not import networkx."
            raise ImportError(msg) from e

        if not isinstance(nx_graph, nx.Graph):
            msg = "nxG must be instance of nx.Graph oder subclasses thereof!"
            raise TypeError(msg)

        is_directed = nx_graph.is_directed()

        try:
            next(iter(nx_graph.nodes))
            nodes = list(range(nx.number_of_nodes(nx_graph)))
            node_labels, node_attributes = zip(*nx_graph.nodes(data=True), strict=False)
            node_labels = dict(zip(nodes, node_labels, strict=False))
        except StopIteration:
            nodes = []
            node_labels, node_attributes = {}, []

        label_map = {label: node for node, label in node_labels.items()}
        try:
            next(iter(nx_graph.edges()))
            u_s, v_s, edge_attributes = zip(*nx_graph.edges(data=True), strict=False)
        except StopIteration:
            u_s, v_s, edge_attributes = [], [], []

        edges = [(label_map[u], label_map[v]) for u, v in zip(u_s, v_s, strict=False)]

        return cls(nodes, node_labels, node_attributes, edges, edge_attributes, is_directed)

    @classmethod
    def from_graph_tool(cls, gt_graph, labelname=None) -> Self:
        """Converts graph-tool Object to Graph.

        Args:
             gt_graph (:class:`graph_tool.Graph`): graph-tool Graph object
             labelname: None or vertex_attribute
                 if None node labels will be set equal to vertex-indices.
                 otherwise a vertex-attribute, that contains the node labels can be set.

        Returns:
             Graph object
        """
        try:
            import graph_tool
        except (ModuleNotFoundError, ImportError) as e:
            msg = "Could not import graph_tool."
            raise ImportError(msg) from e

        if not isinstance(gt_graph, graph_tool.Graph):
            msg = "gtG must be an instance of graph_tool.Graph() !"
            raise TypeError(msg)

        is_directed = gt_graph.is_directed()

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
            next(gt_graph.edges())
            gt_edges, edge_attributes = zip(*create_edges(gt_graph), strict=False)
        except StopIteration:
            gt_edges, edge_attributes = [], []

        try:
            next(gt_graph.vertices())
            gt_nodes, node_attributes = zip(*create_nodes(gt_graph), strict=False)
        except StopIteration:
            gt_nodes, node_attributes = [], []

        if len(gt_nodes) == 0:
            return cls([], [], {}, [], [], is_directed)

        # create name-map for nodes
        nodemap = dict(zip(gt_graph.vertices(), gt_graph.get_vertices(), strict=False))
        if labelname:
            node_labels = dict(
                zip(gt_graph.get_vertices(), gt_graph.vertex_properties[labelname], strict=False),
            )
            nodes = list(node_labels.keys())
        else:
            node_labels = {i: i for i in gt_graph.get_vertices()}
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

        return cls(nodes, node_labels, node_attributes, edges, edge_attributes, is_directed)

    @classmethod
    def from_igraph(cls, igraph_graph) -> Self:
        """Converts igraph-Graph to Graph object.

        Args:
            igraph_graph (:class:`igraph.Graph`): The igraph-Graph to convert.

        Returns:
            An InterGraph instance.
        """
        try:
            import igraph
        except (ModuleNotFoundError, ImportError) as e:
            msg = "Could not import igraph."
            raise ImportError(msg) from e

        if not isinstance(igraph_graph, igraph.Graph):
            msg = "iG must be instance of igraph.Graph() !"
            raise TypeError(msg)

        is_directed = igraph_graph.is_directed()

        # check if edges are present
        try:
            edges, edge_attributes = zip(
                *((e.tuple, e.attributes()) for e in igraph_graph.es()),
                strict=False,
            )
        except ValueError:
            edges, edge_attributes = [], ()

        # check if nodes are present
        try:
            nodes, node_attributes = zip(
                *((n.index, n.attributes()) for n in igraph_graph.vs()),
                strict=False,
            )
        except ValueError:
            nodes, node_attributes = [], ()

        node_labels = {}
        for node, node_attrs in zip(nodes, node_attributes, strict=False):
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
        """Converts Graph object to networkX Graph.

        Args:
            NOT IMPLEMENTED use_labels: choose whether to use labels or indices as names for the
            nodes. If no specific labels were read in, these to are equal.

        Returns:
            networkX Graph, DiGraph, MultiGraph or MultiDiGraph
        """
        try:
            import networkx as nx
        except (ModuleNotFoundError, ImportError) as e:
            msg = "Could not import networkx."
            raise ImportError(msg) from e

        # is multi?
        is_multigraph = len(self.edges) > len(set(self.edges))

        # select appropriate networkX-Graph-Type
        if self.is_directed and not is_multigraph:
            nx_graph = nx.DiGraph()
        elif not self.is_directed and not is_multigraph:
            nx_graph = nx.Graph()
        elif not self.is_directed and is_multigraph:
            nx_graph = nx.MultiGraph()
        else:
            nx_graph = nx.MultiDiGraph()

        nx_graph.add_nodes_from(
            zip((self.node_labels[n] for n in self.nodes), self.node_attributes, strict=False),
        )

        for edge, edge_attr in zip(self.edges, self.edge_attributes, strict=False):
            u, v = edge
            nx_graph.add_edge(self.node_labels[u], self.node_labels[v], **edge_attr)

        return nx_graph

    def to_graph_tool(self, labelname=None):
        """Converts Graph object to graph-tool Graph.

        Args:
            labelname: name for vertex_attribute None, defaults to None.
                if node labels should be kept as vertex attribute,
                the name for the vertex attribute can be specified this way.
        """
        try:
            import graph_tool
        except (ModuleNotFoundError, ImportError) as edge:
            msg = "Could not import graph_tool."
            raise ImportError(msg) from edge

        gt_graph = graph_tool.Graph(directed=self.is_directed)

        if len(self.nodes) == 0:
            return gt_graph

        attrs = {}
        node_type = infer_type(self.node_labels.values(), as_vector=False)

        if labelname:
            attrs[labelname] = gt_graph.new_vertex_property(node_type)

        nodes = {}
        node_property_type_assertion = defaultdict(set)

        for nx_node, data in zip(self.nodes, self.node_attributes, strict=False):
            v = gt_graph.add_vertex()
            if labelname:
                attrs[labelname][v] = self.node_labels[nx_node]
            nodes[nx_node] = v

            for key, val in data.items():
                # Single Type assertion
                node_property_type_assertion[key].add(type(val))
                if len(node_property_type_assertion[key]) > 1:
                    msg = (
                        f"Type not equal for all nodes on Node-Attribute {key}, \
                        types found: {node_property_type_assertion[key]}",
                    )
                    raise PyIntergraphCompatibilityError(msg)

                if key not in attrs:
                    as_vector = isinstance(val, abc.Iterable) and not isinstance(val, str)
                    attrs[key] = gt_graph.new_vertex_property(infer_type(val, as_vector=as_vector))

                attrs[key][v] = val

        for attr_name, attr_val in attrs.items():
            gt_graph.vertex_properties[attr_name] = attr_val

        attrs = {}
        edge_property_assertion = defaultdict(set)
        for edge, data in zip(self.edges, self.edge_attributes, strict=False):
            u, v = edge
            edge = gt_graph.add_edge(nodes[u], nodes[v])
            for key, val in data.items():
                # Single Type assertion
                edge_property_assertion[key].add(type(val))
                if len(edge_property_assertion[key]) > 1:
                    msg = (
                        f"Type not equal for all edges on Edge-Attribute {key}, \
                        types found: {edge_property_assertion[key]}",
                    )
                    raise PyIntergraphCompatibilityError(msg)

                if key not in attrs:
                    as_vector = isinstance(val, abc.Iterable) and not isinstance(val, str)
                    attrs[key] = gt_graph.new_edge_property(infer_type(val, as_vector=as_vector))

                attrs[key][edge] = val

        for attr_key, attr_val in attrs.items():
            gt_graph.edge_properties[attr_key] = attr_val

        return gt_graph

    def to_igraph(self):
        """Converts InterGraph to an igraph-Graph.

        Raises:
            ImportError: raise if igraph is not imported.
            PyIntergraphCompatibilityException: raised if name is a node attribute.

        Returns:
            :class:`igraph.Graph`: Converted igraph-Graph instance.
        """
        try:
            import igraph
        except (ModuleNotFoundError, ImportError) as e:
            msg = "Could not import igraph."
            raise ImportError(msg) from e

        igraph_graph = igraph.Graph(directed=self.is_directed)

        use_labels = True

        try:
            label_type = type(next(iter(self.node_labels)))
        except StopIteration:
            return igraph_graph

        if issubclass(label_type, numbers.Number):
            use_labels = False

        for i, (node, attr) in enumerate(zip(self.nodes, self.node_attributes, strict=False)):
            if use_labels is True:
                igraph_graph.add_vertex(self.node_labels[node], **attr)
            else:
                if "name" in attr:
                    msg = (
                        "Your network seems to have 'name' as a node attribute. "
                        "This is a reserved keyword for node labels in python-igraph. "
                        "You cannot use that!"
                    )
                    raise PyIntergraphCompatibilityError(msg)
                igraph_graph.add_vertex()
                igraph_graph.vs[i].update_attributes(name=self.node_labels[node], **attr)

        for edge, attr in zip(self.edges, self.edge_attributes, strict=False):
            u, v = edge
            # Handle for weird 'name' or 'Vertex-ID' input in igraph
            if use_labels is True:
                u = self.node_labels[u]
                v = self.node_labels[v]

            igraph_graph.add_edge(u, v, **attr)

        return igraph_graph