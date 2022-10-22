import textwrap
import pytest

from data_structures.graph import Graph as graph

if __name__ == "__main__":
  pytest.main([__file__])


class Graph(graph):
  """Updated graph implementation for testability."""

  class Node(graph.Node):
    """Updated Node implementation with new hash method."""

    def __hash__(self):
      """Custom hash method for testability. Not required in main module."""
      return ord(self.value.lower()) - ord("a")


class TestGraph:

  @pytest.fixture
  def node_labels(self) -> list[str]:
    start = ord("A")
    end = start + 4
    return [chr(i) for i in range(start, end)]

  @pytest.fixture
  def new_graph(self) -> Graph:
    return Graph()

  @pytest.fixture
  def graph(self, node_labels: list[str]) -> Graph:
    graph = Graph()
    for node in node_labels:
      graph.add_node(node)
    return graph

  @pytest.fixture
  def connected_graph(self, graph: Graph, node_labels: list[str]):
    for _from in node_labels:
      for _to in node_labels:
        if _from == _to:
          continue
        graph.add_edge(_from, _to)
    return graph

  @pytest.fixture
  def traversal_graph(self, graph: Graph):
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("A", "D")
    graph.add_edge("B", "A")
    graph.add_edge("B", "D")
    graph.add_edge("D", "A")
    graph.add_edge("D", "C")
    return graph

  @pytest.fixture
  def topological_graph(self, graph: Graph):
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")
    return graph

  @pytest.fixture
  def cyclic_graph(self, graph: Graph):
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")
    graph.add_edge("D", "A")
    return graph

  def test_graph_to_str(self, new_graph: Graph):
    assert str(new_graph) == ""
    new_graph.add_node("A")
    new_graph.add_node("B")
    new_graph.add_node("C")
    new_graph.add_node("D")
    assert str(new_graph) == textwrap.dedent("""\
      A: []
      B: []
      C: []
      D: []""")
    new_graph.add_edge("A", "B")
    new_graph.add_edge("A", "C")
    new_graph.add_edge("B", "D")
    new_graph.add_edge("D", "C")

    assert str(new_graph) == textwrap.dedent("""\
      A: ['B', 'C']
      B: ['D']
      C: []
      D: ['C']""")

  def test_graph_has_node(self, graph: Graph, node_labels: list[str]):
    for node in node_labels:
      assert graph.has_node(node)

  def test_graph_add_node(self, new_graph: Graph, node_labels: list[str]):
    for node in node_labels:
      assert new_graph.has_node(node) == False
      new_graph.add_node(node)
      assert new_graph.has_node(node)

  def test_graph_add_duplicate_node(self, graph: Graph, node_labels: list[str]):
    for node in node_labels:
      assert graph.has_node(node)
      graph.add_node(node)

  def test_graph_remove_node(self, graph: Graph, node_labels: list[str]):
    for node in node_labels:
      assert graph.has_node(node)
      assert node in graph.adjacency_list
      graph.remove_node(node)
      assert graph.has_node(node) == False
      assert node not in graph.adjacency_list

  def test_graph_remove_nonexistent_node(self, new_graph: Graph,
                                         node_labels: list[str]):
    for node in node_labels:
      assert new_graph.has_node(node) == False
      new_graph.remove_node(node)

  def test_graph_add_edge(self, graph: Graph, node_labels: list[str]):
    for _from in node_labels:
      for _to in node_labels:
        if _from == _to:
          continue
        assert graph.has_edge(_from, _to) == False
        graph.add_edge(_from, _to)
        assert graph.has_edge(_from, _to)

  def test_graph_add_nonexistent_node_edge(self, graph: Graph):
    with pytest.raises(KeyError):
      graph.add_edge("A", "Z")

    with pytest.raises(KeyError):
      graph.add_edge("Z", "A")

  def test_graph_remove_edge(self, connected_graph: Graph,
                             node_labels: list[str]):
    for _from in node_labels:
      for _to in node_labels:
        if _from == _to:
          continue
        assert connected_graph.has_edge(_from, _to)
        connected_graph.remove_edge(_from, _to)
        assert connected_graph.has_edge(_from, _to) == False

  def test_graph_remove_nonexistent_edge(self, new_graph: Graph):
    new_graph.remove_edge("A", "Z")
    new_graph.remove_edge("Z", "A")

  def test_graph_dfs(self, traversal_graph: Graph, new_graph: Graph):
    assert traversal_graph.dfs() == ["A", "B", "D", "C"]
    assert traversal_graph.dfs("A") == ["A", "B", "D", "C"]
    assert traversal_graph.dfs("B") == ["B", "A", "C", "D"]
    assert traversal_graph.dfs("C") == ["C"]
    assert traversal_graph.dfs("D") == ["D", "A", "B", "C"]
    assert traversal_graph.dfs("N") == []

    assert new_graph.dfs() == []

  def test_graph_iterative_dfs(self, traversal_graph: Graph, new_graph: Graph):
    assert traversal_graph.dfs() == traversal_graph.iterative_dfs()
    assert traversal_graph.dfs("A") == traversal_graph.iterative_dfs("A")
    assert traversal_graph.dfs("B") == traversal_graph.iterative_dfs("B")
    assert traversal_graph.dfs("C") == traversal_graph.iterative_dfs("C")
    assert traversal_graph.dfs("D") == traversal_graph.iterative_dfs("D")
    assert traversal_graph.dfs("N") == traversal_graph.iterative_dfs("N")

    assert new_graph.iterative_dfs() == []

  def test_graph_bfs(self, traversal_graph: Graph, new_graph: Graph):
    assert traversal_graph.bfs() == ["A", "B", "C", "D"]
    assert traversal_graph.bfs("A") == ["A", "B", "C", "D"]
    assert traversal_graph.bfs("B") == ["B", "A", "D", "C"]
    assert traversal_graph.bfs("C") == ["C"]
    assert traversal_graph.bfs("D") == ["D", "A", "C", "B"]
    assert traversal_graph.bfs("N") == []

    assert new_graph.bfs() == []

  def test_graph_topological_sort(self, topological_graph: Graph,
                                  new_graph: Graph):
    assert topological_graph.topological_sort() == ["A", "B", "C", "D"]
    topological_graph.add_node("E")
    topological_graph.add_edge("D", "E")
    assert topological_graph.topological_sort() == ["A", "B", "C", "D", "E"]
    topological_graph.add_edge("E", "A")
    assert topological_graph.topological_sort() == ["A", "B", "C", "D", "E"]

    assert new_graph.topological_sort() == []

  def test_graph_has_cycle(self, topological_graph: Graph, cyclic_graph: Graph,
                           new_graph: Graph):
    assert cyclic_graph.has_cycle()
    cyclic_graph.remove_edge("D", "A")
    assert cyclic_graph.has_cycle() == False

    assert topological_graph.has_cycle() == False
    topological_graph.add_edge("D", "A")
    assert topological_graph.has_cycle()

    assert new_graph.has_cycle() == False


if __name__ == "__main__":
  pytest.main([__file__])
