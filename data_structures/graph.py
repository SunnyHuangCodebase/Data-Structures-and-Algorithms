"""A graph is a network of nodes (or vertices) and their connections (edges).
  Each node (vertex) can connect to any other node(s).
  
  An undirected graph maintains connections between two nodes.
  A directed graph may connect Node A to Node B, but not necessarily B to A.
  Edges may also carry a weight to quantify the connection.
  
  Example of a social network implemented with a graph:
    Nodes represent accounts
    Edges represent followers or friends.
    An undirected graph can indicate friends with an edge. 
    A directed graph can indicate followers with a directed edge.

  This Graph implementation is for instructional purposes.
"""
from __future__ import annotations
from typing import Any


class Graph:
  """Graph implements a graph using a dictionary/hashmap and set implementation.

  Inferior Alternatives:
    An adjacency matrix consumes more memory with no performance gain."""

  class Node:
    """A Graph.Node"""
    value: str

    def __init__(self, value: str):
      self.value = value

    def __str__(self) -> str:
      return self.value

    def __hash__(self):
      """This node implementation uses a custom hash for testability."""
      return ord(self.value.lower()) - ord("a")

  nodes: dict[str, Graph.Node]
  connections: dict[str, set[Graph.Node]]

  def __init__(self):
    self.nodes = {}
    self.connections = {}

  def __str__(self) -> str:
    output: list[str] = []

    for node, edges in self.connections.items():
      output.append(f"{node}: {[edge.value for edge in edges]}")

    return "\n".join(output)

  def has_node(self, node: str):
    """Returns whether a node exists in the graph."""
    return node in self.nodes

  def add_node(self, label: str):
    """Adds a node to the graph."""
    if self.connections.get(label):
      return

    self.nodes[label] = self.Node(label)
    self.connections[label] = set()

  def remove_node(self, label: str):
    """Removes a node from the graph."""
    node = self.nodes.get(label)

    if not node:
      return

    del self.nodes[label]

    edges = self.connections.values()

    for edge in edges:
      try:
        edge.remove(node)
      except KeyError:
        pass

  def has_edge(self, _from: str, _to: str) -> bool:
    """Returns True if there is a connection between two nodes."""
    node = self.nodes.get(_to)
    edges = self.connections.get(_from)

    if not edges or not node:
      return False

    return node in edges

  def add_edge(self, _from: str, _to: str):
    """Adds a connection between two nodes."""

    from_node = self.nodes.get(_from)
    to_node = self.nodes.get(_to)

    if not from_node:
      raise Exception(f"Node '{_from}' doesn't exist")

    if not to_node:
      raise Exception(f"Node '{_to}' doesn't exist")

    edges = self.connections[_from]
    edges.add(to_node)

  def remove_edge(self, _from: str, _to: str):
    """Removes a connection between two nodes."""
    edges = self.connections[_from]
    to_node = self.nodes.get(_to)

    if not edges or not to_node:
      return

    edges.remove(to_node)


class DictGraph:
  nodes: dict[str, DictGraph.Node]
  connections: dict[str, dict[str, DictGraph.Node]]

  class Node:
    name: str

    def __init__(self, name: str):
      self.name = name

  def __init__(self):
    self.connections = {}

  def create_node(self, name: str):
    """Create a node with name."""
    return DictGraph.Node(name)

  def add_node(self, name: str):
    """Adds a node to the graph."""
    if self.connections.get(name):
      return
    self.nodes[name] = self.create_node(name)
    self.connections[name] = {}

  def remove_node(self, name: str):
    """Removes a node from the graph."""
    if not self.connections.get(name):
      return

    del self.connections[name]

    for node in self.connections:
      del self.connections[node][name]

  def add_edge(self, _from: str, _to: str):
    """Adds a connection between two nodes."""
    if not self.nodes.get(_from):
      raise Exception(f"Node {_from} does not exist")
    if not self.nodes.get(_to):
      raise Exception(f"Node {_to} does not exist")
    self.connections[_from] = {_to: self.nodes[_to]}

  def remove_edge(self, _from: str, _to: str):
    """Removes a connection between two nodes."""
    del self.connections[_from][_to]

  def print_graph(self):
    """Prints the graph"""
    nodes: list[str] = []
    for node, connections in self.connections.items():
      nodes.append(f"{node} connections: {list(connections.keys())}")

    print("\n".join(nodes))


class AdjacencyMatrixGraph:
  """A graph that stores node edges/connections in an adjacency matrix.
  
  Vertices/Nodes:
  Each node is assigned to an index.
  nodes: dict[int, Node] = {0: Node(0),
                            1: Node(1)}
                            2: Node(2)}
                            3: Node(3)}
                            4: Node(4)}
  Node N has an index of [N]
  Node 1 has an index of [1]
  Node 2 has an index of [2]
  ...
  
  Edges/Connections:
  Edges between nodes n and m is represented by the data in edges[n][m].

                            #0  1  2  3  4
  edges: list[list[int]] = ([0, 1, 0, 1, 0],  # 0
                            [0, 0, 0, 0, 1],  # 1 
                            [0, 1, 0, 1, 0],  # 2
                            [1, 0, 0, 0, 0],  # 3
                            [1, 1, 1, 1, 0])  # 4
  Characteristics of the above adjacency matrix:
    A directed edge exists from Nodes n to m where edges[n][m] = 1.
    No edge exists between Nodes n and m where edges[n][m] = 0.
    Node 0 [0] has a uni-directional edge to Node 1 [1]. Node 1 has no edge to Node 0.
    Node 0 and Node 3 share a bi-directional edge.
    Node 4 is connected to all other nodes except itself.
    There is a 0 at every intersection where n == m.
    Space Complexity: O(n^2), where n is the number of nodes.
  """

  class Node:
    """An adjacency matrix node."""
    value: Any

  def get_node(self, key: int):
    """Returns the node at self.nodes[key].
    
    Time Complexity: O(1)
    """

  def add_or_remove_node(self, key: int):
    """Adds or removes a node from the adjacency matrix and resizes it.    
    
    Resizing the adjacency matrix is the most expensive method of the operation.

    Time Complexity: O(n), where n is the number of nodes.
      Best Case - O(n) if resizing a dynamic array  
      Worst Case - O(n^2) if resizing a fixed array.
    
    """

  def add_or_remove_edge(self, _from: int, _to: int):
    """Adds or removes an edge between two nodes.

    Time Complexity: O(1)
    """

  def find_edge(self, _from: int, _to: int):
    """Returns an edge between two nodes.

    Time Complexity: O(1)
    """

  def find_neighbors(self, key: int):
    """Returns all of a node's edges.

    This operation iterates through an entire row for matches.
    
    Time Complexity: O(n), where n is the number of nodes.
    """


class AdjacencyListGraph:
  """A graph that stores node edges/connections in an adjacency list.

  Vertices/Nodes:
  Each node is assigned to an index.
  nodes: dict[int, Node] = {0: Node(0),
                            1: Node(1)}
                            2: Node(2)}
                            3: Node(3)}
                            4: Node(4)}
  Node N has an index of [N]
  Node 1 has an index of [1]
  Node 2 has an index of [2]
  ...
  
  Edges/Connections:
  Edges are stored in a list of ListNodes called edges.
  Node n's edges can be found by accessing edges[n].
  Each Node is a ListNode with a "next" field pointing to the next Node.

  edges: list[Node | None] = [
                        Node(2) -> Node(3),             # 0
                        Node(3),                        # 1
                        None,                           # 2
                        Node(0) -> Node(1) -> Node(2)   # 3
                      ]
  Characteristics of the above adjacency matrix:
    Node 1 has a single, uni-directional edge to Node 3.
    Node 2 has no edges.
    Node 3 is connected to all other nodes except itself.
    Node 0 and 3 share a bi-directional edge.

    Space Complexity: O(n + e), where n = # of nodes and e = # of edges.
      Worst Case: O(n^2), where all nodes are interconnected = (n * (n - 1)) = n^2
  """

  class ListNode:
    """An adjacency list node."""
    value: Any
    next: AdjacencyListGraph.ListNode

  def get_node(self, key: int):
    """Returns the node at self.nodes[key].
    
    Time Complexity: O(1)
    """

  def add_node(self, key: int):
    """Adds node to the adjacency list.

    Time Complexity: O(1)   
    """

  def remove_node(self, key: int):
    """Removes a node from the adjacency list and connections to it.
    
    Time Complexity: O(n + e), where n = # of nodes, m = e of edges

      Worst Case: O(n^2), where all nodes are interconnected.
    """

  def add_or_remove_edge(self, _from: int, _to: int):
    """Iterates through all edges _from connects to, then adds or removes _to.

    Time Complexity: O(e), where e = # of edges of _from node.
    Worst Case: O(n), where _from is connected to all other nodes.
    """

  def find_edge(self, _from: int, _to: int):
    """Iterates through all of _from's edges for _to, then returns if it exists.

    Time Complexity: O(e), where e = # of edges of _from node.
    Worst Case: O(n), where _from is connected to all other nodes.
    """

  def find_neighbors(self, key: int):
    """Returns all of a node's edges.
   
    Time Complexity: O(e), where e = # of edges of _from node.
    Worst Case: O(n), where node is connected to all other nodes.
    """
