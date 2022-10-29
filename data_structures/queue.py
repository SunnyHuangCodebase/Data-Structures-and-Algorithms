"""A queue is a FIFO (last in, first out) data sequence.
  The first value to be inserted is the first to be retrieved/removed.

  These Queue implementations are for instructional purposes.

  Python already contains a built-in queue:
    from queue import Queue
    queue = Queue(maxsize=5)

  A deque can also be used:
    from collections import deque

  Queues can be represented by a singly linked list for performance benefits.
  Using a circular array has similar performance and is more memory efficient. 
"""
from typing import Any, Generic, Protocol, TypeVar

from data_structures.linked_list import LinkedList
from data_structures.stack import Stack

T = TypeVar("T")


class Queue(Protocol):
  """Queues contain several operations:
  Enqueue - inserts value at the end of the queue.
  Dequeue - removes and returns value at the start of the queue.
  Peek - returns value at the start of the sequence.
  """

  def to_array(self):
    """Returns the array implementation of an array."""

  def enqueue(self, item: Any):
    """Adds an item to the queue (generally at the end)."""

  def dequeue(self):
    """Removes and returns the item at the end of the queue."""

  def peek(self):
    """Returns the item at the end of the queue."""


class LinkedListQueue(Generic[T]):
  """The linked list in this implementation is singly linked.
  Enqueue, dequeue, and peek operations take O(1) time when implemented as a linked list.
  
  Inferior Alternatives:
    A doubly linked list costs more memory with no performance benefit.
    Queue operations also never need access a node's previous node.

    A circular linked list adds unnecessary complexity with no performance benefit.
  """
  linked_list: LinkedList[T]
  size: int
  max_size: int

  def __init__(self, max_size: int):
    self.linked_list = LinkedList()
    self.max_size = max_size
    self.size = 0

  def to_array(self) -> list[T]:
    """Returns array"""
    return self.linked_list.to_array()

  def enqueue(self, item: T):
    """Adds an item to the end of the queue.
    Time Complexity: O(1)
    """
    if self.is_full():
      raise Exception

    self.linked_list.add_tail(item)
    self.size += 1

  def dequeue(self) -> T:
    """Removes an item from the start of the queue.

    Time Complexity: O(1)
    """
    if self.is_empty():
      raise Exception

    node = self.linked_list.head
    self.linked_list.delete_head()
    self.size -= 1
    return node.value

  def peek(self) -> T | None:
    """Returns the item from the start of the queue.
    
    Time Complexity: O(1)
    """
    if self.is_empty():
      raise Exception

    node = self.linked_list.head
    return node.value if node else None

  def is_empty(self):
    return self.size == 0

  def is_full(self):
    """Returns whether the queue is full."""
    return self.size == self.max_size


class ArrayQueue(Generic[T]):
  """A Queue implementation using a circular Array.

  Inferior Alternatives:
    An static array's dequeue method takes O(n) time.
    A dynamic array's dequeue (and sometimes enqueue*) method takes O(n) time.
  
    *Depends on the implementation.  
  """
  _array: list[T | None]
  _size: int
  _max_size: int
  _start: int
  _end: int

  def __init__(self, max_size: int) -> None:
    self._array = [None] * max_size
    self._size = 0
    self._start = 0
    self._end = 0
    self._max_size = max_size

  def to_array(self) -> list[T | None]:
    return self._array

  def enqueue(self, value: T):
    """Adds an item to the end of the queue."""
    if self.is_full():
      raise Exception("Queue full")

    i = self._end % self._max_size
    self._array[i] = value
    self._size += 1
    self._end += 1

  def dequeue(self) -> T:
    """Removes an item from the start of the queue."""
    if self.is_empty():
      raise Exception("Queue empty")

    i = self._start % self._max_size
    value = self._array[i]

    self._array[i] = None
    self._size -= 1
    self._start += 1
    return value    #type: ignore

  def peek(self) -> T | None:
    """Returns the item from the start of the queue."""
    if self.is_empty():
      raise Exception

    i = self._start % self._max_size
    return self._array[i]

  def is_empty(self):
    """Returns whether the queue is empty."""
    return self._size == 0

  def is_full(self):
    """Returns whether the queue is full."""
    return self._size == self._max_size

  def _adjust_index(self, index: int) -> int:
    """Calculates the circular array's index."""
    return index % self._max_size    #type: ignore


class StackQueue(Generic[T]):
  """A Queue implementation using two stacks."""
  enqueue_stack: Stack[T]
  dequeue_stack: Stack[T]

  def __init__(self, size: int) -> None:
    self.enqueue_stack = Stack(size)
    self.dequeue_stack = Stack(size)

  def enqueue(self, item: T):
    """Adds an item to the end of the queue.
    
    Time Complexity: O(1)
    """
    self.enqueue_stack.push(item)

  def dequeue(self) -> T:
    """Removes an item from the start of the queue.
    
    Time Complexity:

      Best Case - O(1) if dequeue stack has values.
      Worst Case - O(n) if reinitializing stacks
    """

    self.reinitialize_stacks()

    return self.dequeue_stack.pop()

  def peek(self) -> T | None:
    """Returns the item from the start of the queue.
    
    Time Complexity:

      Best Case - O(1) if dequeue stack has values.
      Worst Case - O(n) if reinitializing stacks
    """
    self.reinitialize_stacks()

    return self.dequeue_stack.peek()

  def reinitialize_stacks(self):
    """Fill empty dequeue stack with enqueue stack values, if any."""
    if self.dequeue_stack.is_empty:

      if self.enqueue_stack.is_empty:
        raise Exception("Queue empty")

      while not self.enqueue_stack.is_empty:
        self.dequeue_stack.push(self.enqueue_stack.pop())


class PriorityQueue(ArrayQueue[int]):
  """A subclass of ArrayQueue that allows ordering items in a queue."""

  def enqueue(self, value: int):
    """Enqueue item and then sort the priority queue.
    
    Time Complexity: O(n)

      Best Case - O(1) if enqueued item is the largest value in the queue.
      Worst Case - O(n) if enqueued item is the smallest value in the queue.
    """
    super().enqueue(value)

    if self._size <= 1:
      return

    self._sort()

  def _sort(self):
    """Sort priority queue in ascending order.

    Time Complexity: O(n)

      Best Case - O(1) if queue is already in order.
      Worst Case - O(n) if swapping items from the end to the front of the queue.
    """
    for i in range(self._end - 1, self._start, -1):

      i = self._adjust_index(i)
      current_value, previous_value = self._array[i], self._array[i - 1]

      if current_value > previous_value:    #type: ignore
        break

      self._array[i], self._array[i - 1] = previous_value, current_value
