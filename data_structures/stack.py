"""A stack is a LIFO (last in, first out) data sequence.
  Stack operations only work with the last item of the sequence.

  This Stack implementation is for instructional purposes.
  It can be represented with an array or linked list implementation.
"""
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Stack(Generic[T]):
  """A data structure  """
  _data: list[T] = field(default_factory=list)

  def to_array(self) -> list[T]:
    return self._data

  def push(self, item: T):
    """Adds an item to the end of the stack.

    Time Complexity: O(1)
    """
    self._data.append(item)

  def pop(self) -> T | None:
    """Removes and returns the item at the end of the stack.

    Time Complexity: O(1)
    """
    if not self._data:
      return None

    return self._data.pop()

  def peek(self) -> T | None:
    """Returns the item at the end of the stack.

    Time Complexity: O(1)
    """
    if not self._data:
      return None

    return self._data[-1]

  @property
  def is_empty(self) -> bool:
    """Returns whether the stack has any items.
    
    Time Complexity: O(1)
    """

    return not self._data
