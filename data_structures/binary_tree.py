"""A tree is a heirarchical data structure of nodes.
Each node within the tree can have up to two children.
The top-most node of the tree is the root.
Any node that does not have children are leaves.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar

N = TypeVar("N", "TreeNode", "AVLNode")
T = TypeVar("T", "BinarySearchTree", "AVLTree")


@dataclass
class Node(ABC, Generic[N]):
  """"""
  value: int
  _left: N | None = None
  _right: N | None = None

  def __repr__(self):
    strings: list[str] = []
    if self.value:
      strings.append(f"Node(value = {self.value}")

    if self.left:
      strings.append(f", left = {self.left}")

    if self.right:
      strings.append(f", right = {self.right}")

    if strings:
      strings.append(")")

    return "".join(strings)

  def __str__(self):
    return f"{self.value}"

  @property
  def left(self) -> N | None:
    """Returns left node."""
    return self._left

  @left.setter
  def left(self, node: N | None):
    """Set or delete left node."""
    self._left = node

  @property
  def right(self) -> N | None:
    """Returns right node."""
    return self._right

  @right.setter
  def right(self, node: N | None):
    """Set or delete right node."""
    self._right = node


@dataclass
class TreeNode(Node["TreeNode"]):
  value: int
  _left: TreeNode | None = None
  _right: TreeNode | None = None


@dataclass
class AVLNode(Node["AVLNode"]):
  value: int
  _left: AVLNode | None = None
  _right: AVLNode | None = None
  height: int = 0


@dataclass
class BinaryTree(ABC, Generic[N]):
  """A tree is a data structure containing a root node which can contain subtrees."""

  root: N | None = field(default=None)

  @abstractmethod
  def find(self, value: int) -> bool:
    """"""

  @abstractmethod
  def insert(self, value: int):
    """"""

  def __eq__(self, other: T) -> bool:    # type: ignore
    """Returns whether two trees are equal."""
    return self._equal(self.root, other.root)    # type: ignore

  def _equal(self, node: N | None, other: N | None) -> bool:
    """Iterates through both trees simultaneously to compare equality of all nodes."""

    if not node and not other:
      return True

    if not node or not other or node.value != other.value:
      return False

    return self._equal(node.left, other.left) and self._equal(
        node.right, other.right)

  def is_leaf(self, node: N):
    """Return whether node is a leaf (no children)."""
    return not node.left and not node.right

  def bfs(self):
    """Traverses nodes by row, left to right."""
    nodes = [self.root]
    for node in nodes:
      if not node:
        return

      print(node.value)

      if node.left:
        nodes.append(node.left)

      if node.right:
        nodes.append(node.right)

  def pre_order_dfs(self):
    """Iterates the tree using pre-order DFS starting from the root."""
    self._pre_order_dfs(self.root)

  def _pre_order_dfs(self, root: N | None):
    """Traverses nodes in order of: root, left, right."""
    if not root:
      return

    print(root.value)
    self._pre_order_dfs(root.left)
    self._pre_order_dfs(root.right)

  def in_order_dfs(self):
    """Iterates the tree using in-order DFS starting from the root."""
    self._in_order_dfs(self.root)

  def _in_order_dfs(self, root: N | None):
    """Traverses nodes in order of: left, root, right.
    In a BST, this will traverse nodes in ascending order.
    """
    if not root:
      return

    self._in_order_dfs(root.left)
    print(root.value)
    self._in_order_dfs(root.right)

  def post_order_dfs(self):
    """Iterate the tree using post-order DFS starting from the root."""
    self._post_order_dfs(self.root)

  def _post_order_dfs(self, node: N | None):
    """Traverses nodes in order of: left, right, right.
    This will traverse a tree starting from its leaves first
    """
    if not node:
      return

    self._post_order_dfs(node.left)
    self._post_order_dfs(node.right)
    print(node.value)

  def height(self) -> int:
    """Returns the height of the tree."""
    return self._height(self.root)

  def _height(self, node: N | None) -> int:
    """Returns a node's height, which is equal to the distance from the lowest level.
    The bottommost leaf has a height of 0."""
    if not node:
      return -1

    if not node.left and not node.right:
      return 0

    return 1 + max(self._height(node.left), self._height(node.right))

  def min_value(self):
    """Iterates the entire tree for the minimum value.

    Time Complexity: O(n)
    """
    return self._min_value(self.root)

  def _min_value(self, node: N | None) -> float:
    """Checks every subtree and returns the minimum of the current, left, and right nodes."""
    if not node:
      return float("inf")

    if not node.left and not node.right:
      return node.value

    return min(node.value, self._min_value(node.left),
               self._min_value(node.right))


@dataclass
class BinarySearchTree(BinaryTree[TreeNode]):
  """A tree that meets the following conditions:
    All nodes in the left subtree are smaller than the current node.
    All nodes in the right subtree are greater than the current node.
    All subtrees meet the above conditions and are binary search trees themselves.
  """

  root: TreeNode | None = field(default=None)

  def __repr__(self):
    return f"{self.root}"

  def __eq__(self, other: BinarySearchTree) -> bool:    #type: ignore
    """Returns whether two trees are equal."""
    return super()._equal(self.root, other.root)

  def is_valid(self) -> bool:
    """Iterates the tree to confirm it is a binary search tree, starting from the root."""
    return self._is_valid_node(self.root, float('-inf'), float("inf"))

  def _is_valid_node(self, node: TreeNode | None, min_range: float,
                     max_range: float) -> bool:
    """Checks all nodes to ensure the tree is a valid binary search tree."""
    if not node:
      return True

    if not min_range <= node.value <= max_range:
      return False

    return self._is_valid_node(node.left, min_range, node.value)\
      and self._is_valid_node(node.right, node.value, max_range)

  def find(self, value: int) -> bool:
    """Searches the tree for the correct value."""
    node = self.root
    while node:
      if value == node.value:
        return True

      node = node.left if value < node.value else node.right

    return False

  def insert(self, value: int):
    """Inserts a node with the corresponding value at the correct position using an iterative algorithm.

    Time Complexity: O(log(n))
    """

    if not self.root:
      self.root = TreeNode(value)
      return

    node = self.root

    while node:

      if value < node.value:
        if not node.left:
          node.left = TreeNode(value)
          return
        node = node.left

      else:
        if not node.right:
          node.right = TreeNode(value)
          return
        node = node.right

  def min_value(self) -> int:
    """Iterates to the leftmost value to return the minimum value.

    Time Complexity: O(log(n))
    """
    if not self.root:
      raise Exception("Tree is empty")

    node = self.root
    while node.left:
      node = node.left

    return node.value


@dataclass
class AVLTree(BinaryTree[AVLNode]):
  """A self balancing binary search tree."""
  root: AVLNode | None = field(default=None)

  def __eq__(self, other: AVLTree) -> bool:    #type: ignore
    """Returns whether two trees are equal."""
    return self._equal(self.root, other.root)

  def find(self, value: int) -> bool:
    """Searches the tree for the correct value."""
    node = self.root
    while node:
      if value == node.value:
        return True

      node = node.left if value < node.value else node.right

    return False

  def insert(self, value: int):
    """Inserts a node with the corresponding value at the correct position using a recursive algorithm."""
    self.root = self._insert(self.root, value)

  def _insert(self, node: AVLNode | None, value: int) -> AVLNode:
    """A recursive insert method that creates a valid AVL tree."""
    if not node:
      return AVLNode(value)

    if value < node.value:
      node.left = self._insert(node.left, value)
    else:
      node.right = self._insert(node.right, value)

    self.set_height(node)
    return self.balance(node)

  def height_of(self, node: AVLNode | None) -> int:
    """Returns the height of the current node."""
    if not node:
      return -1
    return node.height

  def subtree_height_difference(self, node: AVLNode | None) -> int:
    """Returns the height difference between both sides of the tree."""
    if not node:
      return 0

    return self.height_of(node.right) - self.height_of(node.left)

  def has_left_skew(self, node: AVLNode) -> bool:
    """Returns whether the tree is unbalanced and skewed towards the left."""
    return self.subtree_height_difference(node) < -1

  def has_right_skew(self, node: AVLNode) -> bool:
    """Returns whether the tree is unbalanced and skewed towards the right."""
    return self.subtree_height_difference(node) > 1

  def balance(self, node: AVLNode):
    """Checks the tree for imbalance and corrects them when adding nodes."""
    if self.has_right_skew(node):
      if self.subtree_height_difference(node.right) < 0:
        node.right = self.rotate_clockwise(node.right)
      node = self.rotate_counterclockwise(node)

    elif self.has_left_skew(node):
      if self.subtree_height_difference(node.left) > 0:
        node.left = self.rotate_counterclockwise(node.left)
      node = self.rotate_clockwise(node)

    return node

  def rotate_clockwise(self, node: AVLNode):
    """Rotates nodes clockwise to rebalance tree"""
    new = node.left
    node.left = new.right
    new.right = node

    self.set_height(node)
    self.set_height(new)

    return new

  def rotate_counterclockwise(self, node: AVLNode):
    """Rotates node counterclockwise to rebalance tree."""
    new = node.right
    node.right = new.left
    new.left = node

    self.set_height(node)
    self.set_height(new)

    return new

  def set_height(self, node: AVLNode):
    """Sets the height of the current node."""
    node.height = 1 + max(self.height_of(node.right), self.height_of(node.left))


# if __name__ == "__main__":
#   avl_tree = AVLTree()
#   avl_tree.insert(16)
#   avl_tree.in_order_dfs()
#   avl_tree.insert(8)
#   avl_tree.in_order_dfs()
#   avl_tree.insert(20)
#   avl_tree.in_order_dfs()
#   avl_tree.insert(4)
#   avl_tree.in_order_dfs()
#   avl_tree.insert(12)
#   avl_tree.in_order_dfs()
#   avl_tree.insert(10)
#   avl_tree.in_order_dfs()
#   avl_tree.insert(18)
#   avl_tree.in_order_dfs()
