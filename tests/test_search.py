import pytest
from algorithms.search import Search


class TestSearch:

  @pytest.fixture
  def sorted_array(self) -> list[int]:
    return list(range(10))

  @pytest.fixture
  def unsorted_array(self) -> list[int]:
    return [2, 4, 6, 0, 7, 1, 9, 3, 5, 8]

  def test_linear_search(self, sorted_array: list[int],
                         unsorted_array: list[int]):
    search = Search()
    for i in range(10):
      assert search.linear_search(sorted_array, i) == i

    assert search.linear_search(unsorted_array, 2) == 0
    assert search.linear_search(unsorted_array, 6) == 2
    assert search.linear_search(unsorted_array, 8) == 9
    assert search.linear_search(unsorted_array, 10) == -1

    assert search.linear_search(sorted_array, 10) == -1
    assert search.linear_search([1, 2], 1) == 0
    assert search.linear_search([2, 1], 1) == 1
    assert search.linear_search([], 1) == -1

  def test_iterative_binary_search(self, sorted_array: list[int]):
    search = Search()
    for i in range(10):
      assert search.iterative_binary_search(sorted_array, i) == i
    assert search.iterative_binary_search(sorted_array, 10) == -1
    assert search.iterative_binary_search([1, 2], 1) == 0
    assert search.iterative_binary_search([], 1) == -1

  def test_recursive_binary_search(self, sorted_array: list[int]):
    search = Search()
    for i in range(10):
      assert search.recursive_binary_search(sorted_array, i) == i
    assert search.recursive_binary_search(sorted_array, 10) == -1
    assert search.recursive_binary_search([1, 2], 1) == 0
    assert search.recursive_binary_search([], 1) == -1


if __name__ == "__main__":
  pytest.main([__file__])
