import textwrap
import pytest

from data_structures.graph import Graph

if __name__ == "__main__":
  pytest.main([__file__])


class TestGraph:

  @pytest.fixture
  def node_labels(self) -> list[str]:
    start = ord("A")
    end = start + 5
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
      graph.remove_node(node)
      assert graph.has_node(node) == False

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

  def test_graph_add_nonexistent_node_edge(self, new_graph: Graph):
    with pytest.raises(Exception):
      new_graph.add_edge("A", "D")

    with pytest.raises(Exception):
      new_graph.add_edge("D", "A")

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
    with pytest.raises(KeyError):
      new_graph.remove_edge("A", "D")
    with pytest.raises(KeyError):
      new_graph.remove_edge("D", "A")


if __name__ == "__main__":
  pytest.main([__file__])
