"""A tree is a heirarchical data structure of nodes.
Each node within the tree can have up to two children.
The top-most node of the tree is the root.
Any node that does not have children are leaves.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class TreeNode:
  value: int
  _left: TreeNode | None
  _right: TreeNode | None

  def __init__(self, value: int):
    self.value = value
    self._left = None
    self._right = None

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

  @property
  def left(self):
    return self._left

  @left.setter
  def left(self, value: int):
    self._left = TreeNode(value)

  @property
  def right(self):
    return self._right

  @right.setter
  def right(self, value: int):
    self._right = TreeNode(value)


class BinaryTree(ABC):
  """A tree is a data structure containing a root node which can contain subtrees."""

  root: TreeNode | None

  @abstractmethod
  def find(self, value: int) -> bool:
    """"""

  @abstractmethod
  def insert(self, value: int):
    """"""

  def __eq__(self, other: BinaryTree) -> bool:    #type: ignore
    """Returns whether two trees are equal."""
    return self._equal(self.root, other.root)

  def _equal(self, node: TreeNode | None, other: TreeNode | None) -> bool:
    if not node and not other:
      return True

    if not node or not other:
      return False

    if node.value != other.value:
      return False

    return self._equal(node.left, other.left) and self._equal(
        node.right, other.right)

  def is_leaf(self, node: TreeNode):
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
    self._pre_order_dfs(self.root)

  def _pre_order_dfs(self, root: TreeNode | None):
    """Traverses nodes in order of: root, left, right."""
    if not root:
      return

    print(root.value)
    self._pre_order_dfs(root.left)
    self._pre_order_dfs(root.right)

  def in_order_dfs(self):
    self._in_order_dfs(self.root)

  def _in_order_dfs(self, root: TreeNode | None):
    """Traverses nodes in order of: left, root, right.
    In a BST, this will traverse nodes in ascending order.
    """
    if not root:
      return

    self._in_order_dfs(root.left)
    print(root.value)
    self._in_order_dfs(root.right)

  def post_order_dfs(self):
    self._post_order_dfs(self.root)

  def _post_order_dfs(self, node: TreeNode | None):
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

  def _height(self, node: TreeNode | None) -> int:
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

  def _min_value(self, node: TreeNode | None) -> int | float:
    """Checks every subtree and returns the minimum of the current, left, and right nodes."""
    if not node:
      return float("inf")

    if not node.left and not node.right:
      return node.value

    return min(node.value, self._min_value(node.left),
               self._min_value(node.right))


@dataclass
class BinarySearchTree(BinaryTree):
  """A tree that meets the following conditions:
    All nodes in the left subtree are smaller than the current node.
    All nodes in the right subtree are greater than the current node.
    All subtrees meet the above conditions and are binary search trees themselves.  
  """

  root: TreeNode | None = field(default=None)

  def __repr__(self):
    return f"{self.root}"

  def __eq__(self, other: BinaryTree) -> bool:    #type: ignore
    """Returns whether two trees are equal."""
    return super().__eq__(other)

  def is_valid(self) -> bool:
    return self._is_valid_node(self.root, float('-inf'), float("inf"))

  def _is_valid_node(self, node: TreeNode | None, min_range: float,
                     max_range: float) -> bool:
    if not node:
      return True

    if not min_range <= node.value <= max_range:
      return False
    # if node.left:
    #   if not min_range <= node.left.value <= node.value:
    #     return False

    # if node.right:
    #   if not node.value <= node.right.value <= max_range:
    #     return False

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
    """Inserts a node with the corresponding value at the correct position."""

    if not self.root:
      self.root = TreeNode(value)
      return

    node = self.root

    while node:

      if value < node.value:
        if not node.left:
          node.left = value
          return
        node = node.left

      else:
        if not node.right:
          node.right = value
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


