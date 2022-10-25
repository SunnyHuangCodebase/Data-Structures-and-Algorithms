import pytest
from pytest import CaptureFixture

import textwrap

from data_structures.weighted_graph import NonexistentNode, PathNotFoundError, WeightedGraph

if __name__ == "__main__":
  pytest.main([__file__])


class TestWeightedGraph:

  @pytest.fixture
  def node_labels(self) -> list[str]:
    start = ord("A")
    end = ord("F") + 1
    return [chr(i) for i in range(start, end)]

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
  def new_graph(self) -> WeightedGraph:
    return WeightedGraph()

  @pytest.fixture
  def weighted_graph(self, weighted_edges: list[tuple[str, str, int]],
                     node_labels: list[str]) -> WeightedGraph:
    weighted_graph = WeightedGraph()

    for node in node_labels:
      weighted_graph.add_node(node)

    for source, target, weight in weighted_edges:
      weighted_graph.add_edge(source, target, weight)
    return weighted_graph

  @pytest.fixture
  def complete_graph(
      self, weighted_edges: list[tuple[str, str, int]]) -> WeightedGraph:
    weighted_graph = WeightedGraph()

    start = ord("A")
    end = ord("E") + 1
    node_labels = [chr(i) for i in range(start, end)]
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

  def test_weighted_graph_has_cycle(self, new_graph: WeightedGraph,
                                    weighted_graph: WeightedGraph):
    assert weighted_graph.has_cycle()
    assert new_graph.has_cycle() == False
    for name in [chr(i) for i in range(ord("A"), ord("G"))]:
      new_graph.add_node(name)

    new_graph.add_edge("A", "B", 1)
    new_graph.add_edge("B", "C", 2)
    new_graph.add_edge("D", "E", 3)
    new_graph.add_edge("E", "F", 3)
    new_graph.add_edge("F", "C", 3)
    assert new_graph.has_cycle() == False

    new_graph.add_edge("D", "A", 3)
    assert new_graph.has_cycle()

  def test_weighted_graph_min_spanning_tree(self, capsys: CaptureFixture[str],
                                            complete_graph: WeightedGraph,
                                            new_graph: WeightedGraph,
                                            node_labels: list[str]):
    print(complete_graph.minimum_spanning_tree())
    captured = capsys.readouterr()

    assert captured.out == textwrap.dedent("""\
      A is connected to [B, C]
      B is connected to [A]
      C is connected to [A, D]
      D is connected to [C, E]
      E is connected to [D]
    """)

    print(new_graph.minimum_spanning_tree())

    assert capsys.readouterr().out == "\n"

    for name in node_labels:
      new_graph.add_node(name)

    print(new_graph.minimum_spanning_tree())

    assert capsys.readouterr().out == "\n"


if __name__ == "__main__":
  pytest.main([__file__])
