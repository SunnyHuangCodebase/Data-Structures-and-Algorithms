import pytest

from algorithms.sort import BubbleSort, InsertionSort, MergeSort, SelectionSort


class TestSort:

  @pytest.fixture
  def numbers(self) -> list[int]:
    return [7, 9, 1, 4, 2, 0, 6, 3, 8, 5]

  @pytest.fixture
  def ascending_order(self) -> list[int]:
    return list(range(10))

  @pytest.fixture
  def descending_order(self) -> list[int]:
    return list(range(9, -1, -1))

  def test_bubble_sort_ascending(self, numbers: list[int],
                                 ascending_order: list[int]):
    sorter = BubbleSort()
    assert sorter.sort(numbers) == ascending_order
    assert sorter.sort([2, 1]) == [1, 2]
    assert sorter.sort([1]) == [1]
    assert sorter.sort([]) == []

  def test_bubble_sort_descending(self, numbers: list[int],
                                  descending_order: list[int]):
    sorter = BubbleSort()
    assert sorter.sort(numbers, descending=True) == descending_order
    assert sorter.sort([1, 2], descending=True) == [2, 1]
    assert sorter.sort([1], descending=True) == [1]
    assert sorter.sort([], descending=True) == []

  def test_selection_sort_ascending(self, numbers: list[int],
                                    ascending_order: list[int]):
    sorter = SelectionSort()
    assert sorter.sort(numbers) == ascending_order
    assert sorter.sort([2, 1]) == [1, 2]
    assert sorter.sort([1]) == [1]
    assert sorter.sort([]) == []

  def test_selection_sort_descending(self, numbers: list[int],
                                     descending_order: list[int]):
    sorter = SelectionSort()
    assert sorter.sort(numbers, descending=True) == descending_order
    assert sorter.sort([1, 2], descending=True) == [2, 1]
    assert sorter.sort([1], descending=True) == [1]
    assert sorter.sort([], descending=True) == []

  def test_insertion_sort_ascending(self, numbers: list[int],
                                    ascending_order: list[int]):
    sorter = InsertionSort()
    assert sorter.sort(numbers) == ascending_order
    assert sorter.sort([2, 1]) == [1, 2]
    assert sorter.sort([1]) == [1]
    assert sorter.sort([]) == []

  def test_insertion_sort_descending(self, numbers: list[int],
                                     descending_order: list[int]):
    sorter = InsertionSort()
    assert sorter.sort(numbers, descending=True) == descending_order
    assert sorter.sort([1, 2], descending=True) == [2, 1]
    assert sorter.sort([1], descending=True) == [1]
    assert sorter.sort([], descending=True) == []

  def test_merge_sort_ascending(self, numbers: list[int],
                                ascending_order: list[int]):
    sorter = MergeSort()
    assert sorter.sort(numbers) == ascending_order
    assert sorter.sort([2, 1]) == [1, 2]
    assert sorter.sort([1]) == [1]
    assert sorter.sort([]) == []

  def test_merge_sort_descending(self, numbers: list[int],
                                 descending_order: list[int]):
    sorter = MergeSort()
    assert sorter.sort(numbers, descending=True) == descending_order
    assert sorter.sort([1, 2], descending=True) == [2, 1]
    assert sorter.sort([1], descending=True) == [1]
    assert sorter.sort([], descending=True) == []


if __name__ == "__main__":
  pytest.main([__file__])
