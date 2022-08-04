"""Array
    This module defines and implements an Array for instructional purposes.
    The Python built-in library already implements the array as a list:
        python_list = list() or []

    An array is a contiguous sequence of items in memory.
    Arrays support only one data type (whereas Python lists support multiple).
    Accessing arrays by their index has a runtime complexity of O(1).
    Traversing an array takes O(n) time.
"""

from typing import Any


class Array:
    """An array contains a sequence of values.
    Each value is mapped to indices starting at 0, incremented by 1.

    Although an array can be visually represented by a list, it can also be represented by a dict.
    This module implements the dict representation, although examples may contain either.

    The arrays are equivalent despite different representation:

        array_dict = {
            0: <First Item>,
            1: <Second Item>,
            2: <Third Item>
        }

        array_list = [<First Item>, <Second Item>, <Third Item>]

    Accessing both arrays with the same key produces same result:
        array_dict[n] == array_list[n]
        *n is a number from 0 to 2.
    """
    data_type: type
    values: dict

    def __init__(self, data_type: type, values: list = []):
        self.data_type = data_type
        self.values: dict[int, self.data_type] = dict(enumerate(values))

    @property
    def size(self) -> int:
        """Returns the length of the array."""
        return len(self.values)

    def __repr__(self):
        return str(list(self.values.values()))

    def swap(self, index_1, index_2):
        """Swaps array values at two indices."""
        self.values[index_1], self.values[index_2] = self.values[index_2], self.values[index_1]

    def bubble_up(self, target_index):
        """Moves a value from the end of array to the target index."""
        current_index = self.size - 1
        while current_index > target_index:
            self.swap(current_index, current_index-1)
            current_index -= 1

    def bubble_down(self, current_index):
        """Moves a value from the current index towards the end of array."""
        target_index = self.size - 1
        while current_index < target_index:
            self.swap(current_index, current_index+1)
            current_index += 1

    def insert(self, value: Any, index: int = float('inf')):
        """Inserts value at specified index and shifts subsequent items right.
        If no array index specified, add value to end of array.

        Time Complexity:
        Best case: O(1) when inserting at end of array.
        Worst case: O(n) when inserting at start of array.

        Example of inserting 2 to array index (i) = 1:
            Array a:                [1, 3, 4]
            Add placeholder:        [1, 3, 4]       -> [1, 3, 4, None]
            Shift items right:      [1, 3, 4, None] -> [1, 3, None, 4]
            Stop when a[i]=None     [1, 3, None, 4] -> [1, None, 3, 4]
            Set a[i] to 2:          [1, None, 3, 4] -> [1, 2, 3, 4]

        The following algorithm produces the same result as the steps above.
        """

        # Check that value's type matches array data type.
        if not isinstance(value, self.data_type):
            print(f"Cannot add {type(value)} to an array of {self.data_type}!")
            return

        if index < 0:
            index = self.size + index

        index = min(index, self.size)
        index = max(0, index)

        self.values[self.size] = value
        self.bubble_up(index)

    def delete_index(self, index: int):
        """Deletes value at specified index and shift subsequent items left.

        Time Complexity: O(n-index)
        Best case: O(1) when deleting from the end of array.
        Worst case: O(n) when deleting from the start of array.

        Example of deleting a value at array index (i) = 1:
            Array a:                [1, 2, 3, 4]
            Delete a[i]:            [1, 2, 3, 4] -> [1, None, 3, 4]
            Shift items left:       [1, None, 2, 4] -> [1, 3, None, 4]
            Stop when a[end]=None:  [1, 3, None, 4] -> [1, 3, 4, None]
            Remove None:            [1, 3, 4, None] -> [1, 3, 4]

        The following algorithm produces the same result as the steps above.
        """

        if index < 0:
            index = self.size + index

        index = min(index, self.size)
        index = max(0, index)

        self.swap(index, self.size - 1)
        del self.values[self.size - 1]
        self.bubble_down(index)

    def delete_value(self, search_value):
        """Deletes the first matching value and shifts the array.

        Time Complexity:
        Search and Delete: O(i), where array[i] = search value
        Shift array: O(n-i)
        Total: O(n)
        """
        if search_value not in self.values.values():
            print(f"Could not find {search_value} in array.")
            return

        for index, value in self.values.items():
            if search_value == value:

                self.swap(self.size - 1, index)
                del self.values[self.size - 1]
                self.bubble_down(index)
                return

    def push(self, value):
        """Inserts a value at the end of array (last index).
            Time Complexity: O(1)
        """
        self.insert(value)

    def pop(self):
        """Returns and removes the value at the end of array (last index).
            Time Complexity: O(1)
        """
        value = self.values[self.size-1]
        self.delete_index(self.size-1)
        return value

