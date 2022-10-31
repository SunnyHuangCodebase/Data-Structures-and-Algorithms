import math


class Search:

  def linear_search(self, array: list[int], target: int) -> int:
    """Searches for target value by iterating through all values in an array.

    Time Complexity: O(n)
      Best Case: O(1) if item is at the start of array.
      Worst Case: O(n) if item is at the end of array.
    """
    for i, value in enumerate(array):
      if value == target:
        return i
    return -1

  def iterative_binary_search(self, array: list[int], target: int) -> int:
    """Repeatedly halves a sorted array at the midpoint to find a target value.

      Calculates the midpoint of a sorted array and checks its value.
      If the target value equals the midpoint value, return the index.
      If the target value is greater, repeat the search on the array's right half.
      Otherwise, repeat the search on the array's left half.
      If no value found, return -1.

    Time Complexity: O(log(n))
    """
    left = 0
    right = len(array)

    i = (left + right) // 2

    while left < right:
      value = array[i]

      if value == target:
        return i

      if value < target:
        left = i + 1

      else:
        right = i

      i = (left + right) // 2

    return -1

  def recursive_binary_search(self, array: list[int], target: int) -> int:
    """Repeatedly halves a sorted array at the midpoint to find the target value.

    Same algorithm as the iterative approach, but using a recursive call stack.
    """
    return self._recursive_binary_search(array, target, 0, len(array) - 1)

  def _recursive_binary_search(self, array: list[int], target: int, left: int,
                               right: int) -> int:
    """The recursive implementation of binary search."""

    if left > right:
      return -1

    i = (left + right) // 2
    value = array[i]

    if value == target:
      return i

    if value < target:
      return self._recursive_binary_search(array, target, i + 1, right)

    else:
      return self._recursive_binary_search(array, target, left, i - 1)

  def ternary_search(self, array: list[int], target: int):
    """Repeatedly divides a sorted array into three to find a target value.
    
    Divides sorted array into partitions equal to the square root of array length.
    Checks if target is within range of the leftmost partition.
    If target value is larger, search next partition to the right.
    If target value is within range, iterate through partition.
    Otherwise, target is not in the array.

    Time Complexity: O(sqrt(n))."""
    return self._ternary_search(array, target, 0, len(array) - 1)

  def _ternary_search(self, array: list[int], target: int, left: int,
                      right: int) -> int:

    if left > right:
      return -1

    partition_size = (right - left) // 3
    mid1 = left + partition_size
    mid2 = right - partition_size

    value1 = array[mid1]
    value2 = array[mid2]

    if target == value1:
      return mid1

    if target == value2:
      return mid2

    if target < value1:
      return self._ternary_search(array, target, left, mid1 - 1)

    if target > value2:
      return self._ternary_search(array, target, mid2 + 1, right)

    return self._ternary_search(array, target, mid1 + 1, mid2 - 1)

  def jump_search(self, array: list[int], target: int) -> int:
    """Iterates through partitions of an array to find the target value.
    
    Divides sorted array into partitions equal to the square root of its length.
    Checks if target is within range of the leftmost partition.
    If target value is larger, searches the subsequent partition for target value.
    If target value is within range, iterates through partition for target value.
    Otherwise, target is not in the array.

    Time Complexity: O(sqrt(n)).
    """
    right = partition_size = math.floor(math.sqrt(len(array)))
    return self._jump_search(array, target, 0, right, partition_size)

  def _jump_search(self, array: list[int], target: int, left: int, right: int,
                   partition_size: int) -> int:
    """The recursive implementation of a jump search."""
    if right in range(len(array)) and target > array[right]:
      left, right = right + 1, right + partition_size
      return self._jump_search(array, target, left, right, partition_size)

    if right >= len(array):
      right = len(array) - 1

    if left in range(len(array)) and target >= array[left]:
      for i in range(left, right + 1):
        if array[i] == target:
          return i

    return -1

  def exponential_search(self, array: list[int], target: int):
    """Doubles sorted array's upper limit (i) until target < array[i], then use binary search.
    
      Start searching array with upper limit of 1 (i = 1).
      If target is larger than array[i], double the upper limit index (i *= 2).
      Once target is smaller than array[i], binary search array between indices i//2 and i.
      
      Time Complexity: O(log(n)), where n is the number of values between indices i//2 and i.
    """
    upper_limit = 1

    while upper_limit < len(array) and target > array[upper_limit]:
      upper_limit *= 2

    left = upper_limit // 2
    upper_limit = min(upper_limit, len(array) - 1)
    return self._recursive_binary_search(array, target, left, upper_limit)
