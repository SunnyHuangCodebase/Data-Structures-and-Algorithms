"""A heap is a binary tree whose nodes are the max or min of all nodes below it.

  Max Heap: All node values are greater than its children's values, recursively.
  Min Heap: All node values are less than its children's values respectively.

  This Heap implementation is for instructional purposes.

  Python already contains a built-in heap:
    import heapq
    heap = []
    heapq.heapify(heap)
    for i in range(10)
      heapq.heappush(heap, i)
    while heap:
      heapq.heappop(heap)
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class MaxHeap:
  """MaxHeap implements a heap using a list representation.

  All nodes of a max heap must be greater than either of its children's values, if any.

  Inferior Alternatives:
    A tree costs more memory with no performance gains.
  """
  data: list[int] = field(default_factory=list)

  def insert(self, value: int):
    """Adds a number to the heap.

    Time Complexity: O(log(n))
    """
    self.data.append(value)
    index = len(self.data) - 1
    self.bubble_up(index)

  def peek(self):
    """Returns the top number from the heap."""
    if not self.data:
      raise IndexError
    return self.data[0]

  def remove(self):
    """Removes and returns the top number from the heap.

    Time Complexity: O(log(n))
    """
    if not self.data:
      raise IndexError

    index = len(self.data) - 1
    if index == 0:
      return self.data.pop()

    self.swap(0, index)
    value = self.data.pop()
    self.bubble_down(0)

    return value

  def swap(self, i: int, j: int):
    """Swaps nodes at two specified heap indices."""

    self.data[i], self.data[j] = self.data[j], self.data[i]

  def bubble_up(self, node: int):
    """Recursively reorders a node with its parent until the heap is valid."""

    if self.has_parent(node) and self.data[node] > self.parent(node):
      self.swap(node, self.parent_index(node))
      self.bubble_up(self.parent_index(node))

  def bubble_down(self, node: int):
    """Recursively reorders a node with its greater child until the heap is valid."""
    greater_child = self.greater_child_index(node)
    if self.has_left_child(node) and greater_child:
      self.swap(node, greater_child)
      self.bubble_down(greater_child)

  def greater_child_index(self, root_index: int):
    """Returns index of the child with a value greater than its parent."""
    if not self.has_left_child(root_index):
      return

    root_value = self.data[root_index]

    greater_child_index = self.left_child_index(root_index)
    greater_child_value = self.left_child(root_index)

    if self.has_right_child(root_index) and self.right_child(
        root_index) > greater_child_value:
      greater_child_index = self.right_child_index(root_index)
      greater_child_value = self.right_child(root_index)

    if root_value > greater_child_value:
      return

    return greater_child_index

  def has_parent(self, index: int):
    """Returns whether the current node has a parent."""
    return self.parent_index(index) >= 0

  def parent_index(self, index: int):
    """The calculated index of the current node's parent."""
    return (index - 1) // 2

  def parent(self, index: int):
    """Returns the parent node's value."""
    return self.data[self.parent_index(index)]

  def has_left_child(self, index: int):
    """Returns whether the current node has a left child."""
    return self.left_child_index(index) < len(self.data)

  def left_child_index(self, index: int) -> int:
    """The calculated index of the current node's left child."""
    return 2 * index + 1

  def left_child(self, index: int):
    """Returns the left child's value."""
    return self.data[self.left_child_index(index)]

  def has_right_child(self, index: int):
    """Returns whether the current node has a right child."""
    return self.right_child_index(index) < len(self.data)

  def right_child_index(self, index: int) -> int:
    """The calculated index of the current node's right child."""
    return 2 * index + 2

  def right_child(self, index: int):
    """Returns the right child's value."""
    return self.data[self.right_child_index(index)]

  def reset(self):
    """Clears heap data."""
    self.data.clear()

  def is_max_heap(self):
    """Returns whether the heap is valid."""
    return all([self.is_valid_node(node) for node in self.data])

  def is_valid_node(self, index: int = 0):
    """Returns whether the current node is a valid heap node."""
    if not self.has_left_child(index):
      return True

    greater_child = self.left_child(index)

    if self.has_right_child(index):
      greater_child = max(greater_child, self.right_child(index))

    return self.data[index] >= greater_child

  @classmethod
  def from_heap_list(cls, heap: list[int]):
    """Alternate constructor method that creates a heap object from a heap list."""
    self = cls()
    self.data = heap
    return self

  @classmethod
  def heapify_list(cls, unordered_list: list[int]):
    """Alternate constructor method that creates a heap from an unordered list."""
    self = cls()
    for number in unordered_list:
      self.insert(number)
    return self

  @staticmethod
  def bubble_up_heapify(array: list[int]):
    """Heapifies a list with the bubble up method."""
    for index in range(len(array)):
      MaxHeap._bubble_up_heapify(array, index)
    return array

  @staticmethod
  def bubble_down_heapify(array: list[int]):
    """Heapifies a list with the bubble down method."""
    for index in range(len(array) // 2 - 1, -1, -1):
      MaxHeap._bubble_down_heapify(array, index)
    return array

  @staticmethod
  def _bubble_up_heapify(array: list[int], index: int):
    """Recursive bubble up heapify method."""
    parent = (index - 1) // 2

    while index and array[index] > array[parent]:

      array[index], array[parent] = array[parent], array[index]
      MaxHeap._bubble_up_heapify(array, parent)

  @staticmethod
  def _bubble_down_heapify(array: list[int], index: int):
    """Recursive bubble down heapify method."""
    larger_index = index

    left_index = 2 * index + 1
    if left_index < len(array) and array[left_index] > array[larger_index]:
      larger_index = left_index

    right_index = 2 * index + 2
    if right_index < len(array) and array[right_index] > array[larger_index]:
      larger_index = right_index

    if index != larger_index:
      array[index], array[larger_index] = array[larger_index], array[index]
      MaxHeap._bubble_down_heapify(array, larger_index)

    index = larger_index

  @staticmethod
  def kth_largest_item(array: list[int], k: int):
    """Return the kth largest item in an array by creating a heapified list."""
    if k not in range(1, len(array) + 1):
      raise IndexError
    heap = MaxHeap()
    for number in array:
      heap.insert(number)

    for _ in range(k - 1):
      heap.remove()

    return heap.peek()
