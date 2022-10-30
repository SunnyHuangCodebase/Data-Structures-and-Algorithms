class Search:
  def linear_search(self, array:list[int], target: int) -> int:
    """Searches for target value by iterating through all values in an array.
    
    Time Complexity: O(n)
      Best Case: O(1) if item is at the start of array.
      Worst Case: O(n) if item is at the end of array.
    """
    for i, value in enumerate(array):
      if value == target:
        return i
    return -1

  def iterative_binary_search(self, array:list[int], target: int) -> int:
    """Searches the middle of a shrinking sorted array for a value.
    
      Search for the value at the middle index of a sorted array.
      If the target value equals the value, return the index.
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

  def recursive_binary_search(self, array:list[int], target: int) -> int:
    """Searches the middle of a shrinking sorted array for a value.
    
    Uses the same algorithm as the iterative approach, but uses a recursive call stack.
    """
    return self._recursive_binary_search(array, target, 0, len(array))

  def _recursive_binary_search(self, array:list[int], target: int, left: int| None = None, right: int| None = None) -> int:
    """The recursive implementation of binary search."""
    left = left or 0
    right = right or len(array)

    if left >= right:
      return -1
    
    i = (left + right) // 2 
    value = array[i]

    if value == target:
      return i
    
    if value < target:
      return self._recursive_binary_search(array, target, i + 1, right)

    else:
      return self._recursive_binary_search(array, target, left, i)

    
