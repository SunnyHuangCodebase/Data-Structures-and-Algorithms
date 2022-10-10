"""A stack is a LIFO (last in, first out) data sequence.
  The last value to be inserted is the first to be retrieved/removed.

  This Stack implementation is for instructional purposes.

  Stacks can be represented with an array or linked list implementation.
  This Stack uses a fixed-size list as a static array for performance benefits.

  

"""
from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
  """Stacks insert (push), remove (pop), and return (peek) values at the end of their sequence.

  These operations benefit from O(1) runtime when implemented as a static array.
  In other words, push, pop, and peek in a static array are nearly instantaneous.

  The array in this implementation is a list of fixed size.

  Inferior Alternatives:
  A regular list is dynamic and "resizes" itself when the number of values exceeds capacity. 
  This costly "resize" operation actually copies values to a new list, taking O(n) time.

  A circular linked list costs more memory with no additional performance gains.
  """
  _data: list[T | None]
  _index: int
  _size: int

  def __init__(self, size: int) -> None:
    self._data = [None for _ in range(size)]
    self._index = 0
    self._size = size

  def to_array(self) -> list[T]:

    return [value for value in self._data if value is not None]

  def push(self, item: T):
    """Adds an item to the end of the stack.

    Time Complexity: O(1)
    """
    try:
      self._data[self._index] = item
      self._index += 1
    except IndexError:
      raise

  def pop(self) -> T:
    """Removes and returns the item at the end of the stack.

    Time Complexity: O(1)
    """
    value = self._data[self._index - 1]

    if not self._index or value is None:
      raise IndexError

    self._index -= 1
    return value

  def peek(self) -> T:
    """Returns the item at the end of the stack.

    Time Complexity: O(1)
    """
    value = self._data[self._index - 1]

    if not self._index or value is None:
      raise IndexError

    return value

  @property
  def is_empty(self) -> bool:
    """Returns whether the stack has any items.
    
    Time Complexity: O(1)
    """

    return not self._index
