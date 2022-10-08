import weakref
import pytest

from data_structures.linked_list import LinkedList, Node


class TestArray:

  @pytest.fixture
  def linked_list(self) -> LinkedList[int]:
    linked_list: LinkedList[int] = LinkedList(Node(1))
    linked_list.add_tail(2)
    linked_list.add_tail(3)
    linked_list.add_tail(4)
    return LinkedList.from_list([1, 2, 3, 4])

  def test_linked_list_alt_constructor(self, linked_list: LinkedList[int]):
    alternate_linked_list = LinkedList.from_list(list(range(1, 5)))
    assert linked_list.to_array() == alternate_linked_list.to_array()

  def test_linked_list_construct_from_linked_node(self):
    second_node = Node(0)
    first_node = Node(1, second_node)
    linked_list = LinkedList(first_node)

    assert linked_list.head == first_node
    assert linked_list.tail == second_node

  def test_linked_list(self, linked_list: LinkedList[int]):
    assert linked_list.head and (linked_list.head.value == 1)
    assert linked_list.tail and (linked_list.tail.value == 4)
    assert linked_list.size() == 4

  def test_linked_list_add_head(self, linked_list: LinkedList[int]):
    assert linked_list.size() == 4
    linked_list.add_head(0)
    assert linked_list.head and (linked_list.head.value == 0)
    assert linked_list.tail and (linked_list.tail.value == 4)
    assert linked_list.size() == 5

  def test_linked_list_add_tail(self, linked_list: LinkedList[int]):
    assert linked_list.size() == 4
    linked_list.add_tail(5)
    assert linked_list.head and (linked_list.head.value == 1)
    assert linked_list.tail and (linked_list.tail.value == 5)
    assert linked_list.size() == 5

  def test_linked_list_delete_head(self, linked_list: LinkedList[int]):
    assert linked_list.size() == 4
    linked_list.delete_head()
    assert linked_list.head and (linked_list.head.value == 2)
    assert linked_list.tail and (linked_list.tail.value == 4)
    assert linked_list.size() == 3

  def test_linked_list_delete_tail(self, linked_list: LinkedList[int]):
    assert linked_list.size() == 4
    linked_list.delete_tail()
    assert linked_list.head and (linked_list.head.value == 1)
    assert linked_list.tail and (linked_list.tail.value == 3)
    assert linked_list.size() == 3

  def test_linked_list_garbage_collector(self):

    linked_list = LinkedList.from_list([1, 2, 3])

    initial_head = weakref.ref(linked_list.head)
    initial_tail = weakref.ref(linked_list.tail)

    assert initial_head() == Node(1, next=Node(2, next=Node(3)))
    assert initial_tail() == Node(3, None)

    linked_list.delete_head()

    assert initial_head() == None
    assert initial_tail() == Node(3, None)

    linked_list.delete_tail()

    assert initial_head() == None
    assert initial_tail() == None

  def test_linked_list_contains(self, linked_list: LinkedList[int]):
    assert linked_list.contains(0) == False
    assert linked_list.contains(1) == True

  def test_linked_list_index(self, linked_list: LinkedList[int]):
    assert linked_list.index_of(0) == -1
    assert linked_list.index_of(1) == 0
    assert linked_list.index_of(4) == 3

  def test_empty_linked_list_add_head(self):
    linked_list: LinkedList[int] = LinkedList()
    assert linked_list.head == linked_list.tail
    linked_list.add_head(0)
    assert linked_list.head == linked_list.tail

  def test_empty_linked_list_add_tail(self):
    linked_list: LinkedList[int] = LinkedList()
    assert linked_list.head == linked_list.tail
    linked_list.add_tail(5)
    assert linked_list.head == linked_list.tail

  def test_linked_list_delete_empty(self):
    linked_list: LinkedList[int] = LinkedList()
    assert linked_list.head == linked_list.tail
    linked_list.delete_head()
    assert linked_list.head == linked_list.tail
    linked_list.delete_tail()
    assert linked_list.head == linked_list.tail

  def test_linked_list_delete_single_node_head(self):
    linked_list: LinkedList[int] = LinkedList(Node(1))
    assert linked_list.head == linked_list.tail
    linked_list.delete_head()
    assert linked_list.head == linked_list.tail == None

  def test_linked_list_delete_single_node_tail(self):
    linked_list: LinkedList[int] = LinkedList(Node(1))
    assert linked_list.head == linked_list.tail
    linked_list.delete_tail()
    assert linked_list.head == linked_list.tail == None


if __name__ == "__main__":
  pytest.main([__file__])
