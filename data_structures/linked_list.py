"""A linked list is a sequence of items containing values of a single data type.
  
  This LinkedList implementation is for instructional purposes.

  Python contains a built-in module that can represent a linked list:
    from collections import deque
    py_linked_list = deque([1, 2, 3, 4])
  
  Note: A linked list can be singly-linked, doubly-linked, or circular.

  This module implements a singly-linked list while a deque is a doubly linked list.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
  value: T
  next: Node[T] | None = field(default=None)


class LinkedList(Generic[T]):
  """A non-cyclical linked list containing a series of nodes."""
  _head: Node[T] | None
  _tail: Node[T] | None
  _size: int

  def __init__(self, node: Node[T] | None = None):
    self._head = node
    self._size = 0

    if node:
      self._size += 1
      while node.next:
        node = node.next

    self._tail = node

  def to_array(self) -> list[T]:
    """Returns a list representation of the linked list."""
    node = self._head
    nodes: list[T] = []
    while node:
      nodes.append(node.value)
      node = node.next

    return nodes

  @property
  def head(self):
    return self._head

  @property
  def tail(self):
    return self._tail

  def size(self) -> int:
    """Returns the size of the linked list."""
    return self._size

  def add_head(self, value: T):
    """Adds a value to the beginning of the linked list.
        
    Time Complexity: O(1)
    """
    node = Node(value)
    self._size += 1

    if not self._head:
      self._head = self._tail = node
      return

    self._head, self._head.next = node, self._head

  def add_tail(self, value: T):
    """Adds a value to the end of the linked list.
        
    Time Complexity: O(1)
    """
    node = Node(value)
    self._size += 1

    if not self._head:
      self._head = self._tail = node
      return

    self._tail.next = self._tail = node

  def delete_head(self):
    """Deletes the first value of the linked list.
    
    Time Complexity: O(1)
    """
    if not self._head:
      return

    self._size -= 1

    if self._head == self._tail:
      self._head = self._tail = None
      return

    self._head = self._head.next

  def delete_tail(self):
    """Deletes the last value of the linked list.

    Time Complexity: O(n)
    """

    if not self._head:
      return

    self._size -= 1

    if self._head == self._tail:
      self._head = self._tail = None
      return

    node = self._head

    while node.next and node.next != self._tail:
      node = node.next

    self._tail, self._tail.next = node, None

  def contains(self, value: T):
    """Returns whether the linked list contains a node with the requested value.
    
    Time Complexity: O(n)

      Best Case - O(1) when the node is at the linked list's head.
      Worst Case - O(n) when the node is at the linked list's tail.
    """
    node = self._head
    while node:
      if node.value == value:
        return True
      node = node.next

    return False

  def index_of(self, value: T):
    """Returns the index of the node with the requested value.
    
    Time Complexity: O(n)

      Best Case - O(1) when the node is at the linked list's head.
      Worst Case - O(n) when the node is at the linked list's tail.
    """
    node = self._head
    index = 0
    while node:
      if node.value == value:
        return index
      node = node.next
      index += 1

    return -1

  @classmethod
  def from_list(cls, node_value_list: list[T]) -> LinkedList[T]:
    """Generates a linked list from a list of node values."""
    self = cls()
    for value in node_value_list:
      self.add_tail(value)
    return self
