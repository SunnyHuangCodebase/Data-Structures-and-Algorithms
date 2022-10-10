"""An array is a sequence containing values of a single data type.
  This Array implementation is for instructional purposes.

  Python already contains a built-in array:
    from array import array
    py_array = array("i", [1, 2, 3, 4])

  Alternatively, a list can also represent an array:
    py_array = []

  Note: Python lists can support multiple types.
"""

from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class Array(Generic[T]):
  """An array contains a sequence of values of type (T) accessible by their index.
  T can be any type, as long as all array values of the same type.
  """
  # An array represented by a dictionary containing index keys and values.
  _values: dict[int, T]
  _index: int

  # An array made up of list values. Less explicit than a dictionary.
  # values: list[T]

  def __init__(self, values: Iterable[T]) -> None:
    self._values = dict(enumerate(values, start=0))
    self._index = 0
    # enumerate() has a default start value of 0. Included for explicitness.

  def __len__(self) -> int:
    """Returns length of array values by calling len(array)."""
    return len(self._values)

  def __getitem__(self, index: int):
    """Returns value at array index with array[index].

    Time Complexity: O(1)
    """
    return self._values[index]

  def __setitem__(self, index: int, value: T):
    """Sets value at array index with array[index] = value.

    Time Complexity: O(1)
    """
    self._values[index] = value

  def __iter__(self):
    """Along with __next__, enables iterating over array."""
    return self

  def __next__(self):
    """Enables iterating over an array or calling next(array)."""

    value = self._values.get(self._index, None)

    if value is None:
      self._index = 0
      raise StopIteration

    self._index += 1

    return value

  def __repr__(self) -> str:
    return f"{list(self._values.values())}"

  def size(self) -> int:
    """Returns the length of the array."""
    return len(self._values)

  def push(self, value: T, index: int | None = None):
    """Inserts value at array index after shifting subsequent values to the right.
    
    If no index is provided, inserts at the end of array.
    
    Time Complexity: O(n)

      Best Case - O(1) when inserting at the end of array.
      Worst Case - O(n) when inserting at the start of array.
    """

    index = self.size() if index is None else index

    if index not in range(self.size() + 1):
      raise IndexError

    self._values[self.size()] = value

    for i in range(self.size() - 1, index, -1):
      self._values[i], self._values[i - 1] = self._values[i -
                                                          1], self._values[i]

  def pop(self, index: int | None = None):
    """Removes a value from the array and shifts subsequent values to the left.

    If no index is provided, remove the value at the end of array.
    
    Time Complexity: O(n)

      Best Case - O(1) when removing from the end of array.
      Worst Case - O(n) when removing from the start of array.
    """
    index = self.size() - 1 if index is None else index

    if index not in range(self.size()):
      raise IndexError

    value = self._values[index]

    for i in range(index, self.size() - 1):
      self._values[i] = self._values[i + 1]

    del self._values[self.size() - 1]

    return value

  def index_of(self, search_value: T):
    """Searches array for a value and returns the first index where it occurs.
    
    Time Complexity: O(n)

      Best Case - O(1) when the value is at the start of array.
      Worst Case - O(n) when inserting at the end of the array.
    """
    for index, value in self._values.items():
      if value == search_value:
        return index

    return -1
