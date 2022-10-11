import pytest

from data_structures.queue import LinkedListQueue, ArrayQueue, StackQueue, PriorityQueue


class TestQueue:

  @pytest.fixture
  def linked_list_queue(self) -> LinkedListQueue[int]:
    return LinkedListQueue(5)

  @pytest.fixture
  def array_queue(self) -> ArrayQueue[int]:
    return ArrayQueue(5)

  @pytest.fixture
  def stack_queue(self) -> StackQueue[int]:
    return StackQueue(5)

  @pytest.fixture
  def priority_queue(self) -> PriorityQueue:
    return PriorityQueue(5)

  def test_linked_list_queue_enqueue(self,
                                     linked_list_queue: LinkedListQueue[int]):
    for i in range(5):
      linked_list_queue.enqueue(i)

    assert linked_list_queue.to_array() == [0, 1, 2, 3, 4]
    assert linked_list_queue.peek() == 0

    with pytest.raises(Exception):
      linked_list_queue.enqueue(5)

    linked_list_queue.dequeue()
    linked_list_queue.dequeue()
    linked_list_queue.enqueue(3)
    assert linked_list_queue.to_array() == [2, 3, 4, 3]
    assert linked_list_queue.peek() == 2

  def test_linked_list_queue_dequeue(self,
                                     linked_list_queue: LinkedListQueue[int]):
    with pytest.raises(Exception):
      linked_list_queue.dequeue()

    for i in range(5):
      linked_list_queue.enqueue(i)

    assert linked_list_queue.dequeue() == 0
    assert linked_list_queue.to_array() == [1, 2, 3, 4]
    assert linked_list_queue.dequeue() == 1
    assert linked_list_queue.to_array() == [2, 3, 4]
    linked_list_queue.enqueue(1)
    assert linked_list_queue.to_array() == [2, 3, 4, 1]

  def test_linked_list_queue_peek(self,
                                  linked_list_queue: LinkedListQueue[int]):
    with pytest.raises(Exception):
      linked_list_queue.peek()

    for i in range(5):
      linked_list_queue.enqueue(i)
      assert linked_list_queue.peek() == 0

    linked_list_queue.dequeue()
    assert linked_list_queue.peek() == 1
    linked_list_queue.dequeue()
    assert linked_list_queue.peek() == 2

  def test_array_queue_enqueue(self, array_queue: ArrayQueue[int]):
    for i in range(5):
      array_queue.enqueue(i)
    assert array_queue.to_array() == [0, 1, 2, 3, 4]
    array_queue.dequeue()
    assert array_queue.to_array() == [None, 1, 2, 3, 4]
    array_queue.dequeue()
    assert array_queue.to_array() == [None, None, 2, 3, 4]

    array_queue.enqueue(5)
    assert array_queue.to_array() == [5, None, 2, 3, 4]
    assert array_queue.peek() == 2

    array_queue.enqueue(0)
    assert array_queue.to_array() == [5, 0, 2, 3, 4]
    assert array_queue.peek() == 2

  def test_array_queue_dequeue(self, array_queue: ArrayQueue[int]):
    with pytest.raises(Exception):
      array_queue.dequeue()

    for i in range(5):
      array_queue.enqueue(i)

    assert array_queue.dequeue() == 0
    assert array_queue.to_array() == [None, 1, 2, 3, 4]
    assert array_queue.dequeue() == 1
    assert array_queue.to_array() == [None, None, 2, 3, 4]
    assert array_queue.dequeue() == 2
    assert array_queue.to_array() == [None, None, None, 3, 4]
    array_queue.enqueue(5)
    assert array_queue.to_array() == [5, None, None, 3, 4]
    assert array_queue.dequeue() == 3
    assert array_queue.dequeue() == 4
    assert array_queue.dequeue() == 5
    assert array_queue.to_array() == [None] * 5

  def test_array_queue_peek(self, array_queue: ArrayQueue[int]):
    with pytest.raises(Exception):
      array_queue.peek()

  def test_stack_queue_enqueue(self, stack_queue: StackQueue[int]):
    for i in range(3):
      stack_queue.enqueue(i)
      assert stack_queue.peek() == 0

    stack_queue.dequeue()
    assert stack_queue.peek() == 1
    stack_queue.dequeue()
    stack_queue.enqueue(3)
    assert stack_queue.dequeue() == 2
    assert stack_queue.peek() == 3

  def test_stack_queue_dequeue(self, stack_queue: StackQueue[int]):
    with pytest.raises(Exception):
      stack_queue.dequeue()

    for i in range(5):
      stack_queue.enqueue(i)

    assert stack_queue.dequeue() == 0
    assert stack_queue.dequeue() == 1
    stack_queue.enqueue(4)
    assert stack_queue.dequeue() == 2
    assert stack_queue.dequeue() == 3
    assert stack_queue.dequeue() == 4
    assert stack_queue.dequeue() == 4

  def test_stack_queue_peek(self, stack_queue: StackQueue[int]):
    with pytest.raises(Exception):
      stack_queue.peek()

    for i in range(5):
      stack_queue.enqueue(i)
      assert stack_queue.peek() == 0

    stack_queue.dequeue()
    assert stack_queue.peek() == 1
    stack_queue.dequeue()
    assert stack_queue.peek() == 2
    stack_queue.dequeue()
    assert stack_queue.peek() == 3

  def test_priority_queue_enqueue(self, priority_queue: PriorityQueue):
    priority_queue.enqueue(5)
    assert priority_queue.to_array() == [5, None, None, None, None]
    priority_queue.enqueue(3)
    assert priority_queue.to_array() == [3, 5, None, None, None]
    priority_queue.enqueue(1)
    assert priority_queue.to_array() == [1, 3, 5, None, None]
    priority_queue.enqueue(2)
    assert priority_queue.to_array() == [1, 2, 3, 5, None]
    priority_queue.enqueue(4)
    assert priority_queue.to_array() == [1, 2, 3, 4, 5]

    with pytest.raises(Exception):
      priority_queue.enqueue(0)

  def test_priority_queue_dequeue(self, priority_queue: PriorityQueue):
    with pytest.raises(Exception):
      priority_queue.dequeue()

    priority_queue.enqueue(5)
    priority_queue.enqueue(3)
    priority_queue.enqueue(1)
    priority_queue.enqueue(2)
    priority_queue.enqueue(4)

    assert priority_queue.dequeue() == 1
    assert priority_queue.to_array() == [None, 2, 3, 4, 5]

    assert priority_queue.dequeue() == 2
    assert priority_queue.to_array() == [None, None, 3, 4, 5]

    priority_queue.enqueue(6)
    assert priority_queue.to_array() == [6, None, 3, 4, 5]

    assert priority_queue.dequeue() == 3
    assert priority_queue.to_array() == [6, None, None, 4, 5]

    priority_queue.enqueue(3)
    assert priority_queue.to_array() == [5, 6, None, 3, 4]
    assert priority_queue.dequeue() == 3
    assert priority_queue.dequeue() == 4
    assert priority_queue.dequeue() == 5
    assert priority_queue.dequeue() == 6
    assert priority_queue.to_array() == [None] * 5

  def test_priority_queue_peek(self, priority_queue: PriorityQueue):
    with pytest.raises(Exception):
      priority_queue.peek()

    priority_queue.enqueue(5)
    assert priority_queue.peek() == 5
    priority_queue.enqueue(3)
    assert priority_queue.peek() == 3
    priority_queue.enqueue(1)
    assert priority_queue.peek() == 1
    priority_queue.enqueue(2)
    assert priority_queue.peek() == 1
    priority_queue.enqueue(4)
    assert priority_queue.peek() == 1

    priority_queue.dequeue()
    assert priority_queue.peek() == 2
    priority_queue.dequeue()
    assert priority_queue.peek() == 3
    priority_queue.dequeue()
    assert priority_queue.peek() == 4
    priority_queue.dequeue()
    assert priority_queue.peek() == 5


if __name__ == "__main__":
  pytest.main([__file__])
