"""A graph is a network of nodes (vertices) and connections (edges).
  A node (vertex) represents an object and may connect to any other node(s) (neighbor(s)).
  Edges behave differently depending on the graph type:
    Undirected: Connects two nodes (A and B).
    Directed: Connects a source (A) to target (B), but not necessarily B to A.
    Weighted: Connects A and B with a weight, which quantifies the connection.
  
  Example of a social network implemented with a graph:
    Nodes represent accounts
    Edges represent various things depending on the graph type:
      Undirected: A and B are mutual friends
      Directed: A is B's follower, but B may not necessarily be A's follower.
      Weighted: The frequency at which A and B interact with each other. 

  This Graph implementation is for instructional purposes.
"""
from __future__ import annotations
from collections import deque
from typing import Any


class Graph:
  """Graph implements a graph using an dictionary/set adjacency list.

    The pros and cons of an adjacency matrix vs adjacency list are discussed later.
  """

  class Node:
    """A Graph.Node"""
    value: str

    def __init__(self, value: str):
      self.value = value

  nodes: dict[str, Graph.Node]
  adjacency_list: dict[str, set[Graph.Node]]

  def __init__(self):
    self.nodes = {}
    self.adjacency_list = {}

  def __str__(self) -> str:
    output: list[str] = []

    for node, neighbors in self.adjacency_list.items():
      output.append(f"{node}: {[neighbor.value for neighbor in neighbors]}")

    return "\n".join(output)

  def _get_node_default(self, name: str | None) -> str | None:
    """Returns the name of a node if it exists, or None if it doesn't.
    
      If node is unspecified, defaults to the name of first node in the graph.
    """
    if not name:
      return self._first_node()

    if not self.has_node(name):
      return None

    return name

  def _first_node(self) -> str | None:
    """Returns the name of the first node in the graph, if any. Otherwise returns None."""
    if not self.nodes:
      return None

    return next(iter(self.nodes))

  def _get_node_by_name(self, name: str) -> Graph.Node | None:
    """Return the node with the specified name or None if it doesn't exist."""
    return self.nodes.get(name)

  def _get_node_edges(self, name: str) -> set[Graph.Node] | None:
    """Returns the edges of a node, if any. Otherwise, returns None."""
    return self.adjacency_list.get(name)

  def has_node(self, name: str | None) -> bool:
    """Returns whether a node exists in the graph."""

    if not self.nodes:
      return False

    return name in self.nodes

  def add_node(self, name: str):
    """Adds a new node to the graph."""

    if self.has_node(name):
      return

    self.nodes[name] = self.Node(name)
    self.adjacency_list[name] = set()

  def remove_node(self, node: str):
    """Removes the node and all references to it from the graph."""
    if not self.has_node(node):
      return

    for source in self.adjacency_list:
      self.remove_edge(source, node)

    del self.nodes[node]
    del self.adjacency_list[node]

  def has_edge(self, source: str, target: str) -> bool:
    """Returns True if there is a connection between two nodes."""
    try:
      return self.nodes[target] in self.adjacency_list[source]
    except KeyError:
      return False

  def add_edge(self, source: str, target: str):
    """Adds a connection between two nodes."""
    edges = self.adjacency_list[source]
    node = self.nodes[target]
    edges.add(node)

  def remove_edge(self, source: str, target: str):
    """Removes a connection between two nodes."""
    try:
      edges = self.adjacency_list[source]
      node = self.nodes[target]
      edges.remove(node)
    except KeyError:
      return

  def dfs(self, root: str | None = None) -> list[str]:
    """Traverses graph in DFS order with a visited set.

      This implementation is recursive and can be converted to an iterative implementation.
      Only one implementation is necessary, but both are included for instructional purposes.
    """
    nodes: list[str] = []

    if root := self._get_node_default(root):
      visited: set[str] = set()
      self._dfs(root, nodes, visited)

    return nodes

  def iterative_dfs(self, root: str | None = None) -> list[str]:
    """Traverses graph in DFS order with a traversal stack and visited set.
    
      This alternative implementation is iterative and is for instructional purposes.
      In production code, exclude implementation details in the method name (i.e., iterative).
    """
    nodes: list[str] = []

    if root := self._get_node_default(root):
      stack: list[str] = [root]
      visited: set[str] = set()

      while stack:
        current = stack.pop()
        self._visit(current, nodes, visited, stack)

    return nodes

  def _visit(self, node: str, nodes: list[str], visited: set[str],
             stack: list[str]):
    """Visits a node and its neighbors to the stack in reverse order.
    
      Reversing the append order is unnecessary in producing a valid DFS order.
      It is only necessary to generate the same output as the recursive DFS for tests.
    """
    if node in visited:
      return

    nodes.append(node)
    visited.add(node)

    for neighbor in reversed(list(self.adjacency_list.get(node, set()))):
      if neighbor.value not in visited:
        stack.append(neighbor.value)

  def _dfs(self, node: str, nodes: list[str], visited: set[str]):
    """Recursive DFS traversal."""
    if node in visited:
      return

    nodes.append(node)
    visited.add(node)

    for neighbor in self.adjacency_list.get(node, {}):
      self._dfs(neighbor.value, nodes, visited)

  def bfs(self, root: str | None = None) -> list[str]:
    """Traverses graph in BFS order with a visiting queue and visited set."""
    nodes: list[str] = []

    if root := self._get_node_default(root):
      queue: deque[str] = deque((root,))
      visited: set[str] = set()

      while queue:
        self._bfs(queue.popleft(), nodes, visited, queue)

    return nodes

  def _bfs(self, current_node: str, nodes: list[str], visited: set[str],
           queue: deque[str]):
    """Recursive BFS traversal."""
    if current_node in visited:
      return

    nodes.append(current_node)
    visited.add(current_node)

    for node in self.adjacency_list.get(current_node, set()):
      if node.value not in visited:
        queue.append(node.value)

  def topological_sort(self) -> list[str]:
    """Returns ordered list where all source nodes precede target nodes in the graph."""
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
    """Recursive topological sort method.."""
    if current_node in visited:
      return

    visited.add(current_node)

    for node in reversed(list(self.adjacency_list.get(current_node, set()))):
      if node.value not in visited:
        self._topological_sort(node.value, visited, stack)

    stack.append(current_node)

  def has_cycle(self) -> bool:
    """Returns whether the graph has a cycle."""
    visiting: set[str] = set()
    visited: set[str] = set()
    for node in self.nodes:
      if self._has_cycle(node, visiting, visited):
        return True
    return False

  def _has_cycle(self, node: str, visiting: set[str],
                 visited: set[str]) -> bool | None:
    """Recursive method to check for a cycle in the graph."""
    if node in visiting:
      return True

    if node in visited:
      return False

    visiting.add(node)

    for edge in self.adjacency_list.get(node, set()):
      if self._has_cycle(edge.value, visiting, visited):
        return True

    visited.add(node)
    visiting.remove(node)

    return False


class DictGraph:
  """A graph implementation using a nested dictionary"""

  class Node:
    name: str

    def __init__(self, name: str):
      self.name = name

  nodes: dict[str, DictGraph.Node]
  adjacency_list: dict[str, dict[str, DictGraph.Node]]

  def __init__(self):
    self.adjacency_list = {}

  def has_node(self, name: str | None) -> bool:
    """Returns whether a node exists in the graph."""

    if not self.nodes:
      return False

    return name in self.nodes

  def add_node(self, name: str):
    """Adds a node to the graph."""
    if self.has_node(name):
      return

    self.nodes[name] = self.Node(name)
    self.adjacency_list[name] = {}

  def remove_node(self, name: str):
    """Removes a node from the graph."""
    if not self.adjacency_list.get(name):
      return

    del self.adjacency_list[name]

    for node in self.adjacency_list:
      del self.adjacency_list[node][name]

  def add_edge(self, _from: str, _to: str):
    """Adds a connection between two nodes."""
    if not self.nodes.get(_from):
      raise Exception(f"Node {_from} does not exist")
    if not self.nodes.get(_to):
      raise Exception(f"Node {_to} does not exist")
    self.adjacency_list[_from] = {_to: self.nodes[_to]}

  def remove_edge(self, _from: str, _to: str):
    """Removes a connection between two nodes."""
    del self.adjacency_list[_from][_to]

  def print_graph(self):
    """Prints the graph"""
    nodes: list[str] = []
    for node, connections in self.adjacency_list.items():
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
