class BubbleSort:

  def sort(self, array: list[int], *, descending: bool = False):
    """Swaps out of order values sequentially by index towards the end of array.

      Time Complexity: O(n^2)
        Best Case - O(n) if array is already sorted.
        Worst Case - O(n^2) if array is sorted in reverse order.
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


class InsertionSort:

  def sort(self, array: list[int], *, descending: bool = False):
    """Repeatedly inserts the next value into the preceding ordered sequence.

    Iterate through array and take note of the current value.
    Ensure current and preceding values form an increasing/decreasing sequence.
    Otherwise, shift preceding items right to find a valid insertion index.

    Time Complexity: O(n^2)
      Best Case - O(n) if array is already sorted.
      Worst Case - O(n^2) if array is sorted in reverse order.
    """
    for index, num in enumerate(array):
      self._insert_in_continuous_sequence(array, num, index, descending)
    return array

  def _insert_in_continuous_sequence(self, array: list[int],
                                     insertion_number: int, last_index: int,
                                     descending: bool):
    """Inserts number into an increasing/decreasing sequence at a valid index."""
    for index in range(last_index - 1, -1, -1):

      if not descending and insertion_number < array[index] or\
        descending and insertion_number > array[index]:
        array[index + 1] = array[index]
      else:
        array[index + 1] = insertion_number
        return

      if index == 0:
        array[index] = insertion_number


class MergeSort:

  def sort(self, array: list[int], *, descending: bool = False) -> list[int]:
    """Recursively divides array into two for sorting and merging.
    
    A divide and conquer algorithm that splits the array into smaller subarrays.
    The subarrays are recursively divided for sorting.
    When subarrays are fully sorted, they are combined with the next subarray.
    Subarrays eventually form the full array of sorted items.

    Time Complexity: O(n * log(n)) even if the array is already sorted.
    Space Complexity: O(n)
    """
    if len(array) <= 1:
      return array

    midpoint = len(array) // 2

    left_array: list[int] = self.sort(array[:midpoint], descending=descending)
    right_array: list[int] = self.sort(array[midpoint:], descending=descending)

    return self.merge_sort(left_array, right_array, descending)

  def merge_sort(self, left_array: list[int], right_array: list[int],
                 descending: bool):
    """Compares each value in two arrays and combines them into a single array."""
    left_index: int = 0
    right_index: int = 0
    combined_array: list[int] = []
    while left_index in range(len(left_array)) and right_index in range(
        len(right_array)):

      left_num = left_array[left_index]
      right_num = right_array[right_index]

      if descending and left_num < right_num or\
        not descending and left_num > right_num:
        combined_array.append(right_num)
        right_index += 1

      else:
        combined_array.append(left_num)
        left_index += 1

    combined_array.extend(left_array[left_index:])
    combined_array.extend(right_array[right_index:])

    return combined_array
