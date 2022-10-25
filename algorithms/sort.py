class BubbleSort:

  def sort(self, array: list[int], *, descending: bool = False):
    """Swaps out of order values sequentially by index towards the end of array.

      Time Complexity: O(n^2)
        Best Case - O(n) when all values are in order.
        Worst Case - O(n^2) when values are in reverse order. 
    """
    end = len(array) - 1

    while end > 0:
      sorted = False

      for i in range(end):
        if self._sort(array, i, i + 1, descending):
          sorted = True

      end -= 1

      if sorted:
        continue

    return array

  def _sort(self, array: list[int], index1: int, index2: int,
            descending_order: bool):
    """Swaps two numbers if they are out of order. If swapped, return False."""

    if not descending_order and array[index1] > array[index2]:
      array[index1], array[index2] = array[index2], array[index1]
      return True

    if descending_order and array[index1] < array[index2]:
      array[index1], array[index2] = array[index2], array[index1]
      return True

    return False


class SelectionSort:

  def sort(self, array: list[int], *, descending: bool = False):
    """Repeatedly swaps next min/max value with next index's value (starting at 0).

      Search array for the min value if descending. Otherwise, find max value.
      Swap the value with the value at the start of the array.
      Shrink the array to exclude the value at the start of the array.
      Repeat from the beginning with the new subarray.

      Time Complexity: O(n^2) even if the array is already sorted.
    """
    end = len(array)

    for start in range(end):
      min_max_index = start
      for index in range(start + 1, end):
        min_max_index = self._get_min_max_index(array, index, min_max_index,
                                                descending)

      array[start], array[min_max_index] = array[min_max_index], array[start]
    return array

  def _get_min_max_index(self, array: list[int], index: int, min_max_index: int,
                         descending: bool):
    """Compares current and min/max index values and returns the new min/max index."""
    if not descending and array[index] < array[min_max_index]:
      return index

    if descending and array[index] > array[min_max_index]:
      return index

    return min_max_index
