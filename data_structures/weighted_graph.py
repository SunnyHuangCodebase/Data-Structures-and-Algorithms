from __future__ import annotations
import heapq


class WeightedGraph:

  class Node:
    value: str
    edges: dict[str, WeightedGraph.Edge]

    def __init__(self, value: str) -> None:
      self.value = value
      self.edges = {}

    def __str__(self):
      return self.value

    def __repr__(self):
      return self.value

    def __lt__(self, other: WeightedGraph.Node):
      return ord(self.value) < ord(other.value)

    def __le__(self, other: WeightedGraph.Node):
      return ord(self.value) <= ord(other.value)

    def __gt__(self, other: WeightedGraph.Node):
      return ord(self.value) > ord(other.value)

    def __ge__(self, other: WeightedGraph.Node):
      return ord(self.value) >= ord(other.value)

    def add_edge(self, node: WeightedGraph.Node, weight: int):
      """Adds a weighted edge to another node."""
      self.edges[node.value] = WeightedGraph.Edge(self, node, weight)

    def get_edges(self):
      return self.edges.values()

  class Edge:
    source: WeightedGraph.Node
    target: WeightedGraph.Node
    weight: int

    def __init__(self, source: WeightedGraph.Node, target: WeightedGraph.Node,
                 weight: int) -> None:
      self.source = source
      self.target = target
      self.weight = weight

    def __str__(self):
      return f"{self.source} -{self.weight})-> {self.target}"

  nodes: dict[str, WeightedGraph.Node]

  def __init__(self):
    self.nodes = {}

  def add_node(self, name: str):
    """Adds a node if it doesn't exist."""
    self.nodes[name] = self.nodes.get(name, self.Node(name))

  def add_edge(self, source: str, target: str, weight: int):
    """Adds a weighted edge between two nodes."""
    source_node = self.nodes[source]
    target_node = self.nodes[target]
    source_node.add_edge(target_node, weight)
    target_node.add_edge(source_node, weight)

  def __str__(self):
    output: list[str] = []
    for node in self.nodes.values():
      output.append(f"{node} is connected to {node.get_edges()}")
    return "\n".join(output)

  def get_shortest_distance(self, source: str, target: str) -> int:
    """Returns the shortest distance between two nodes.

    Uses Djikstra's Algorithm.
    """
    try:
      if not self.nodes[target].get_edges():
        raise PathNotFoundError
    except KeyError:
      raise NonexistentNode

    heap: list[tuple[int, WeightedGraph.Node]] = []
    visited: set[WeightedGraph.Node] = set()
    heapq.heappush(heap, (0, self.nodes[source]))

    while heap:

      weight, node = heapq.heappop(heap)

      if node.value is target:
        return weight

      if node in visited:
        continue

      visited.add(node)

      for edge in node.get_edges():
        heapq.heappush(heap, (weight + edge.weight, edge.target))

    raise PathNotFoundError

  def get_shortest_path(self, source: str, target: str) -> list[str]:
    """Returns the shortest node path between two nodes.

    Uses Djikstra's Algorithm.
    """
    try:
      source_node = self.nodes[source]
      self.nodes[target]
    except KeyError:
      raise NonexistentNode

    routes: dict[WeightedGraph.Node, float] = {}
    priority_queue: list[tuple[float, WeightedGraph.Node]] = []
    visited: set[WeightedGraph.Node] = set()

    for node in self.nodes.values():
      routes[node] = float("inf")

    previous_nodes: dict[str, str] = {}
    routes[source_node] = 0

    heapq.heappush(priority_queue, (0, source_node))

    while priority_queue:
      _, current = heapq.heappop(priority_queue)
      visited.add(current)
      for edge in current.get_edges():
        if edge.target in visited:
          continue
        distance = routes[current] + edge.weight
        if distance < routes[edge.target]:
          routes[edge.target] = distance
          previous_nodes[edge.target.value] = current.value
          heapq.heappush(priority_queue, (distance, edge.target))

    return self._generate_shortest_path(previous_nodes, target)

  def _generate_shortest_path(self, previous_nodes: dict[str, str],
                              target: str) -> list[str]:
    """Converts a reverse sequence of nodes into a node path."""
    path: list[str] = []
    stack: list[str] = []
    stack.append(target)
    previous = previous_nodes.get(target)

    while previous:
      stack.append(previous)
      previous = previous_nodes.get(previous)

    while stack:
      path.append(stack.pop())

    return path


class PathNotFoundError(Exception):
  """Path between two graph nodes not found."""


class NonexistentNode(Exception):
  """Node not found in graph."""
