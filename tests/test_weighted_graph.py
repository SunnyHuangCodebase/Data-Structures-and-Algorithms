import pytest
import textwrap
from pytest import CaptureFixture, MonkeyPatch, TempPathFactory

from data_structures.weighted_graph import NonexistentNode, PathNotFoundError, WeightedGraph


class TestWeightedGraph:

  @pytest.fixture
  def node_labels(self) -> list[str]:
    return [chr(i) for i in range(ord("A"), ord("G"))]

  @pytest.fixture
  def weighted_edges(self) -> list[tuple[str, str, int]]:

    return [
        ("A", "B", 1),
        ("A", "C", 2),
        ("A", "D", 5),
        ("B", "D", 3),
        ("B", "E", 7),
        ("C", "D", 1),
        ("D", "E", 2),
    ]

  @pytest.fixture
  def weighted_graph(
      self, node_labels: list[str],
      weighted_edges: list[tuple[str, str, int]]) -> WeightedGraph:
    weighted_graph = WeightedGraph()

    for node in node_labels:
      weighted_graph.add_node(node)

    for source, target, weight in weighted_edges:
      weighted_graph.add_edge(source, target, weight)
    return weighted_graph

  def test_weighted_graph(self, weighted_graph: WeightedGraph):
    print(weighted_graph)

  def test_weighted_graph_get_shortest_distance(self,
                                                weighted_graph: WeightedGraph):

    assert weighted_graph.get_shortest_distance("A", "A") == 0
    assert weighted_graph.get_shortest_distance("A", "B") == 1
    assert weighted_graph.get_shortest_distance("B", "A") == 1
    assert weighted_graph.get_shortest_distance("A", "C") == 2
    assert weighted_graph.get_shortest_distance("A", "D") == 3
    assert weighted_graph.get_shortest_distance("A", "E") == 5
    assert weighted_graph.get_shortest_distance("B", "D") == 3
    assert weighted_graph.get_shortest_distance("C", "E") == 3

    with pytest.raises(NonexistentNode):
      weighted_graph.get_shortest_distance("A", "G")

    with pytest.raises(PathNotFoundError):
      weighted_graph.get_shortest_distance("A", "F")

  def test_weighted_graph_get_shortest_path(self,
                                            weighted_graph: WeightedGraph):

    assert weighted_graph.get_shortest_path("A", "A") == ["A"]
    assert weighted_graph.get_shortest_path("A", "B") == ["A", "B"]
    assert weighted_graph.get_shortest_path("B", "A") == ["B", "A"]
    assert weighted_graph.get_shortest_path("A", "C") == ["A", "C"]
    assert weighted_graph.get_shortest_path("A", "D") == ["A", "C", "D"]
    assert weighted_graph.get_shortest_path("A", "E") == ["A", "C", "D", "E"]
    assert weighted_graph.get_shortest_path("B", "D") == ["B", "D"]
    assert weighted_graph.get_shortest_path("C", "E") == ["C", "D", "E"]

    with pytest.raises(NonexistentNode):
      weighted_graph.get_shortest_distance("A", "G")

    with pytest.raises(PathNotFoundError):
      weighted_graph.get_shortest_distance("A", "F")


if __name__ == "__main__":
  pytest.main([__file__])
