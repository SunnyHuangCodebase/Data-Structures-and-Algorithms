import pytest

from data_structures.array import Array


class TestArray:

  @pytest.fixture
  def array(self) -> Array[int]:
    return Array([0, 1, 2, 3, 4])

  def test_array_size(self, array: Array[int]):
    assert len(array) == 5

  def test_array_repr(self, array: Array[int]):
    assert f"{array}" == "[0, 1, 2, 3, 4]"

  def test_array_length(self, array: Array[int]):
    assert len(array) == 5

  def test_array_iteration(self, array: Array[int]):
    assert f"{''.join([str(number) for number in array])}" == "01234"

  def test_array_next(self, array: Array[int]):

    assert next(array) == 0
    assert next(array) == 1
    assert next(array) == 2
    assert next(array) == 3
    assert next(array) == 4
    with pytest.raises(StopIteration):
      next(array)

  def test_array_getter(self, array: Array[int]):

    assert array[0] == 0
    assert array[2] == 2
    assert array[4] == 4

  def test_array_setter(self, array: Array[int]):
    array[0] = 1
    assert array[0] == 1

  def test_array_push(self, array: Array[int]):
    array.push(5)
    assert array[5] == 5

  def test_array_push_index(self, array: Array[int]):
    array.push(1, 0)
    assert array[0] == 1

  def test_array_pop(self, array: Array[int]):
    assert array.pop() == 4

  def test_array_pop_index(self, array: Array[int]):
    assert array.pop(0) == 0

  def test_array_pop_out_of_range(self, array: Array[int]):
    with pytest.raises(IndexError):
      array.pop(6)
    with pytest.raises(IndexError):
      array.pop(-1)

  def test_array_push_out_of_range(self, array: Array[int]):
    with pytest.raises(IndexError):
      array.push(1, 6)
    with pytest.raises(IndexError):
      array.push(1, -1)

  def test_array_index_search(self, array: Array[int]):
    assert array.index_of(0) == 0
    assert array.index_of(4) == 4
    assert array.index_of(5) == -1


if __name__ == "__main__":
  pytest.main([__file__])
