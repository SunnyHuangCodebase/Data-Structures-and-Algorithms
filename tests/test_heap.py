import pytest
from data_structures.heap import MaxHeap


class TestHeap:

  @pytest.fixture
  def heap(self) -> MaxHeap:
    heap = MaxHeap()
    for i in range(16):
      heap.insert(i)

    return heap

  @pytest.fixture
  def new_heap(self) -> MaxHeap:
    return MaxHeap()

  def test_heap_insert(self, new_heap: MaxHeap):
    for i in range(5, -1, -1):
      new_heap.insert(i)
      assert new_heap.data[0] == 5

    assert new_heap.data == [5, 4, 3, 2, 1, 0]

    new_heap.reset()

    for i in range(5):
      new_heap.insert(i)
      assert new_heap.data[0] == i

    assert new_heap.data == [4, 3, 1, 0, 2]

  def test_heap_remove(self, heap: MaxHeap):
    for i in range(16):
      assert heap.remove() == 15 - i

  def test_heap_remove_empty(self, new_heap: MaxHeap):
    with pytest.raises(IndexError):
      new_heap.remove()

  def test_heap_peek_empty(self, new_heap: MaxHeap):
    with pytest.raises(IndexError):
      new_heap.peek()

  def test_valid_heap(self, heap: MaxHeap):
    assert heap.is_max_heap()

  def test_invalid_heap(self):
    unordered_list = [4, 1, 2, 3, 46, 8, 5, 12, 15, 21, 14]
    invalid_heap = MaxHeap.from_heap_list(unordered_list)
    assert invalid_heap.is_max_heap() == False

  def test_heapified_list(self):
    heapified_list = MaxHeap.heapify_list(list(range(10)))
    for i in range(10):
      assert heapified_list.remove() == 9 - i

  def test_bubble_up_heapify(self):
    array = list(range(10))
    heapified_list = MaxHeap.bubble_up_heapify(array)
    heap = MaxHeap.from_heap_list(heapified_list)
    assert heap.is_max_heap()

  def test_bubble_down_heapify(self):
    array = list(range(10))
    heapified_list = MaxHeap.bubble_down_heapify(array)
    heap = MaxHeap.from_heap_list(heapified_list)
    assert heap.is_max_heap()

  def test_heap_kth_largest_item(self):
    with pytest.raises(IndexError):
      MaxHeap.kth_largest_item(list(range(10)), 0)
    for i in range(1, 10):
      assert MaxHeap.kth_largest_item(list(range(10)), i) == 10 - i


if __name__ == "__main__":
  pytest.main([__file__])
