"""A graph is a network of nodes (vertices) and their connections (edges).
  A node (vertex) represents an object and may connect to any other node(s).
  
  Edges in an undirected graph represent a connections between two nodes (A and B).
  Edges in a directed graph may connect A to B, but not necessarily B to A.
  Edges may also carry a weight to quantify the connection.
  
  Example of a social network implemented with a graph:
    Nodes represent accounts
    Edges represent followers or friends.
    An undirected graph can indicate friends with an edge. 
    A directed graph can indicate followers with a directed edge.

  This Graph implementation is for instructional purposes.
"""
from __future__ import annotations
from collections import deque
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

  def dfs(self, root: str | None = None) -> list[str]:
    """Traverses through the graph in DFS order with a visited set.
    
    This implementation is recursive and can be converted to an iterative implementation.
    Only one implementation is necessary, but both are included for instructional purposes.
    """
    nodes: list[str] = []
    visited: set[str] = set()
    root = root or list(self.nodes.keys())[0]
    if not self.nodes.get(root):
      return nodes
    self._dfs(root, nodes, visited)
    return nodes

  def iterative_dfs(self, root: str | None = None) -> list[str]:
    """Traverses through the graph in DFS order with a traversal stack and visited set.
    
    This alternative implementation is iterative and is for instructional purposes.
    In production code, exclude implementation details in the method name (i.e., iterative).
    """
    root = root or list(self.nodes.keys())[0]
    nodes: list[str] = []

    if not self.nodes.get(root):
      return nodes

    stack: list[str] = [root]
    visited: set[str] = set()

    while stack:
      current = stack.pop()
      self._visit(current, nodes, visited, stack)

    return nodes

  def _visit(self, current_node: str, nodes: list[str], visited: set[str],
             stack: list[str]):
    """Visits a node and appends edges to the stack in reverse order.
    
    Reversing the append order is unnecessary in producing a valid DFS order.
    It is only necessary to generate the same output as the recursive DFS for tests.
    """
    if current_node in visited:
      return

    nodes.append(current_node)
    visited.add(current_node)

    connections = self.connections.get(current_node)

    if not connections:
      return

    edges = list(connections)
    edges.reverse()

    for node in edges:
      stack.append(node.value)

  def _dfs(self, current_node: str, nodes: list[str], visited: set[str]):
    """Recursive DFS traversal."""
    if current_node in visited:
      return

    nodes.append(current_node)
    visited.add(current_node)

    edges = self.connections.get(current_node)

    if not edges:
      return

    for node in edges:
      self._dfs(node.value, nodes, visited)

  def bfs(self, root: str | None = None) -> list[str]:
    """Traverses through the tree in BFS order with a traversal queue and visited set."""
    root = root or list(self.nodes.keys())[0]
    nodes: list[str] = []

    if not self.nodes.get(root):
      return nodes

    queue: deque[str] = deque()
    visited: set[str] = set()
    queue.append(root)

    while queue:
      current_node = queue.popleft()

      if current_node in visited:
        continue
      nodes.append(current_node)
      visited.add(current_node)
      edges = self.connections.get(current_node)

      if not edges:
        continue

      for edge in edges:
        if edge.value not in visited:
          queue.append(edge.value)

    return nodes

  def topological_sort(self) -> list[str]:
    stack: list[str] = []
    visited: set[str] = set()

    for node in self.nodes:
      self._topological_sort(node, visited, stack)

    nodes: list[str] = []
    while stack:
      nodes.append(stack.pop())
    return nodes

  def _topological_sort(self, current_node: str, visited: set[str],
                        stack: list[str]):
    """"""
    if current_node in visited:
      return

    visited.add(current_node)
    connections = self.connections.get(current_node)

    if not connections:
      stack.append(current_node)
      return

    edges = list(connections)
    edges.reverse()

    for node in edges:
      if node.value not in visited:
        self._topological_sort(node.value, visited, stack)

    stack.append(current_node)

  def has_cycle(self) -> bool:

    visiting: set[str] = set()
    visited: set[str] = set()
    for node in self.nodes:
      if self._has_cycle(node, visiting, visited):
        return True
    return False

  def _has_cycle(self, node: str, visiting: set[str],
                 visited: set[str]) -> bool | None:

    if node in visited:
      return False

    if node in visiting:
      return True

    visiting.add(node)
    connections = self.connections[node]
    edges: list[Graph.Node] = []

    if connections:
      edges = list(connections)

    for edge in edges:
      if self._has_cycle(edge.value, visiting, visited):
        return True

    visited.add(node)
    visiting.remove(node)

    return False


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
  Superior performance only in dense graphs, where nodes have many edges.
  
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
  Superior performance in most cases, except dense graphs.
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
