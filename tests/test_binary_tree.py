import pytest
from pytest import CaptureFixture

from data_structures.binary_tree import BinarySearchTree


class TestBinaryTree:

  @pytest.fixture
  def bst(self) -> BinarySearchTree:
    bst = BinarySearchTree()
    bst.insert(16)
    bst.insert(8)
    bst.insert(20)
    bst.insert(4)
    bst.insert(12)
    bst.insert(10)
    bst.insert(18)
    return bst

  @pytest.fixture
  def bst2(self) -> BinarySearchTree:
    bst = BinarySearchTree()
    bst.insert(16)
    bst.insert(8)
    bst.insert(20)
    bst.insert(4)
    bst.insert(12)
    bst.insert(10)
    bst.insert(18)
    return bst

  @pytest.fixture
  def bst3(self) -> BinarySearchTree:
    bst = BinarySearchTree()
    bst.insert(15)
    bst.insert(8)
    bst.insert(20)
    bst.insert(4)
    bst.insert(12)
    bst.insert(10)
    bst.insert(18)
    return bst

  @pytest.fixture
  def new_tree(self) -> BinarySearchTree:
    return BinarySearchTree()

  def format_print(self, bst_values: list[int]):
    strings: list[str] = []
    for value in bst_values:
      strings.append(str(value))
      strings.append("\n")

    return "".join(strings)

  def test_bst_insert(self, bst: BinarySearchTree):
    bst.insert(1)

  def test_bst_bfs(self, bst: BinarySearchTree, capsys: CaptureFixture[str]):
    bst.bfs()
    captured = capsys.readouterr()
    bfs = [16, 8, 20, 4, 12, 18, 10]
    assert captured.out == self.format_print(bfs)

  def test_bst_pre_order_dfs(self, bst: BinarySearchTree,
                             capsys: CaptureFixture[str]):
    bst.pre_order_dfs()
    captured = capsys.readouterr()
    dfs = [16, 8, 4, 12, 10, 20, 18]
    assert captured.out == self.format_print(dfs)

  def test_bst_in_order_dfs(self, bst: BinarySearchTree,
                            capsys: CaptureFixture[str]):
    bst.in_order_dfs()
    captured = capsys.readouterr()
    dfs = [4, 8, 10, 12, 16, 18, 20]
    assert captured.out == self.format_print(dfs)

  def test_bst_post_order_dfs(self, bst: BinarySearchTree,
                              capsys: CaptureFixture[str]):
    bst.post_order_dfs()
    captured = capsys.readouterr()
    dfs = [4, 10, 12, 8, 18, 20, 16]
    assert captured.out == self.format_print(dfs)

  def test_bst_equality(self, bst: BinarySearchTree, bst2: BinarySearchTree):
    assert bst == bst2

  def test_bst_inequality(self, bst: BinarySearchTree, bst3: BinarySearchTree):
    assert bst != bst3

  def test_bst_is_valid(self, bst: BinarySearchTree):
    assert bst.is_valid()
    bst.root.value = 100
    assert bst.is_valid() == False

  def test_bst_min_value(self, new_tree: BinarySearchTree):
    with pytest.raises(Exception):
      new_tree.min_value()
    for i in range(16, -1, -1):
      new_tree.insert(i)
      assert new_tree.min_value() == i

  def test_bst_find_value(self, new_tree: BinarySearchTree):
    for i in range(16):
      assert new_tree.find(i) == False
      new_tree.insert(i)
      assert new_tree.find(i)

  def test_bst_string_and_repr(self, new_tree: BinarySearchTree):
    new_tree.insert(2)
    new_tree.insert(1)
    new_tree.insert(3)
    new_tree.insert(4)

    assert f"{new_tree.root}" == "2"
    assert f"{new_tree.root!r}" == "TreeNode(value = 2, left = TreeNode(value = 1), right = TreeNode(value = 3, right = TreeNode(value = 4)))"


if __name__ == "__main__":
  pytest.main([__file__])
