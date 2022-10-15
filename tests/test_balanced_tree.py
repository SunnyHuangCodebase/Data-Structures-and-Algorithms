import pytest
from pytest import CaptureFixture

from data_structures.binary_tree import AVLTree


class TestBalancedTree:

  @pytest.fixture
  def avl_tree(self) -> AVLTree:
    avl_tree = AVLTree()
    avl_tree.insert(16)
    avl_tree.insert(8)
    avl_tree.insert(20)
    avl_tree.insert(4)
    avl_tree.insert(12)
    avl_tree.insert(10)
    avl_tree.insert(18)
    return avl_tree

  @pytest.fixture
  def avl_tree2(self) -> AVLTree:
    avl_tree = AVLTree()
    avl_tree.insert(16)
    avl_tree.insert(8)
    avl_tree.insert(20)
    avl_tree.insert(4)
    avl_tree.insert(12)
    avl_tree.insert(10)
    avl_tree.insert(18)
    return avl_tree

  @pytest.fixture
  def avl_tree3(self) -> AVLTree:
    avl_tree = AVLTree()
    avl_tree.insert(15)
    avl_tree.insert(8)
    avl_tree.insert(20)
    avl_tree.insert(4)
    avl_tree.insert(12)
    avl_tree.insert(10)
    avl_tree.insert(18)
    return avl_tree

  @pytest.fixture
  def new_tree(self) -> AVLTree:
    return AVLTree()

  def format_print(self, avl_tree_values: list[int]):
    strings: list[str] = []
    for value in avl_tree_values:
      strings.append(str(value))
      strings.append("\n")

    return "".join(strings)

  def test_avl_tree_insert(self, avl_tree: AVLTree):
    avl_tree.insert(1)

  def test_avl_tree_bfs(self, avl_tree: AVLTree, new_tree: AVLTree,
                        capsys: CaptureFixture[str]):
    avl_tree.bfs()
    captured = capsys.readouterr()
    # bfs = [16, 8, 20, 4, 12, 18, 10]
    bfs = [12, 8, 18, 4, 10, 16, 20]
    assert captured.out == self.format_print(bfs)

  def test_avl_tree_pre_order_dfs(self, avl_tree: AVLTree,
                                  capsys: CaptureFixture[str]):
    avl_tree.pre_order_dfs()
    captured = capsys.readouterr()
    # pre_order_dfs = [16, 8, 4, 12, 10, 20, 18]
    pre_order_dfs = [12, 8, 4, 10, 18, 16, 20]
    assert captured.out == self.format_print(pre_order_dfs)

  def test_avl_tree_in_order_dfs(self, avl_tree: AVLTree,
                                 capsys: CaptureFixture[str]):
    avl_tree.in_order_dfs()
    captured = capsys.readouterr()
    # in_order_dfs = [4, 8, 10, 12, 16, 18, 20]
    in_order_dfs = [4, 8, 10, 12, 16, 18, 20]
    assert captured.out == self.format_print(in_order_dfs)

  def test_avl_tree_post_order_dfs(self, avl_tree: AVLTree,
                                   capsys: CaptureFixture[str]):
    avl_tree.post_order_dfs()
    captured = capsys.readouterr()
    # post_order_dfs = [4, 10, 12, 8, 18, 20, 16]
    post_order_dfs = [4, 10, 8, 16, 20, 18, 12]
    assert captured.out == self.format_print(post_order_dfs)

  def test_empty_avl_tree_traversal(self, new_tree: AVLTree,
                                    capsys: CaptureFixture[str]):
    new_tree.bfs()
    new_tree.pre_order_dfs()
    new_tree.in_order_dfs()
    new_tree.post_order_dfs()
    captured = capsys.readouterr()
    assert captured.out == ""

  def test_avl_tree_equality(self, avl_tree: AVLTree, avl_tree2: AVLTree):
    assert avl_tree == avl_tree2

  def test_avl_tree_inequality(self, avl_tree: AVLTree, avl_tree3: AVLTree):
    assert avl_tree != avl_tree3

  def test_avl_tree_leaf(self, avl_tree: AVLTree):
    node = avl_tree.root
    while node and node.left:
      assert avl_tree.is_leaf(node) == False
      node = node.left
    assert avl_tree.is_leaf(node)

  def test_avl_tree_height(self, new_tree: AVLTree):

    height = -1
    assert new_tree.height() == height
    for i in range(16):
      new_tree.insert(i)
      if i in [0, 1, 3, 7, 15]:
        height += 1
        assert new_tree.height() == height

    node = new_tree.root
    assert new_tree.subtree_height_difference(node) == 1
    while node:
      node = node.left
    assert new_tree.subtree_height_difference(node) == 0

  def test_min_value(self, new_tree: AVLTree):
    assert new_tree.min_value() == float("inf")
    for i in range(16, -1, -1):
      new_tree.insert(i)
      assert new_tree.min_value() == i

  def test_find_value(self, new_tree: AVLTree):
    for i in range(16):
      assert new_tree.find(i) == False
      new_tree.insert(i)
      assert new_tree.find(i)

  def test_avl_tree_string_and_repr(self, new_tree: AVLTree):
    new_tree.insert(2)
    new_tree.insert(1)
    new_tree.insert(3)
    new_tree.insert(4)

    assert f"{new_tree.root}" == "2"
    assert f"{new_tree.root!r}" == "AVLNode(value = 2, left = AVLNode(value = 1), right = AVLNode(value = 3, right = AVLNode(value = 4)))"


if __name__ == "__main__":
  pytest.main([__file__])
