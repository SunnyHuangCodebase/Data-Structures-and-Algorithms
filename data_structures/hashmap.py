"""A hashmap is collection of key-value pairs with efficient operation runtime complexity.
  This Hashmap implementation is for instructional purposes.

  Python already contains a built-in hashmap (dictionary):
    hashmap = {}
"""
from data_structures.linked_list import LinkedList


class Hashmap:
  data: list[LinkedList[tuple[int, str]] | None]
  size: int

  def __init__(self, size: int) -> None:
    self.data = [None for _ in range(size)]
    self.size = size

  def insert(self, key: int, value: str):
    """Inserts a key-value pair into the hashmap for retrieval.
    
    Time Complexity O(1):
      Average Case: O(1) with no collisions.
      Worst Case: O(n) with many collisions.
    """
    index = self.generate_hash(key)
    key_value_pair = (key, value)
    linked_list = self.data[index] = self.data[index] or LinkedList()

    try:
      node = linked_list.head
    except IndexError:
      linked_list.add_tail(key_value_pair)
      return
    finally:
      node = linked_list.head

    while node:
      if node.value[0] != key:
        node = node.next
        continue

      node.value = key_value_pair
      return

    linked_list.add_tail(key_value_pair)

  def get(self, key: int):
    """Return the value associated with the key.
    
    Time Complexity O(1):
      Average Case: O(1) with no collisions.
      Worst Case: O(n) with many collisions.
    """
    index = self.generate_hash(key)
    linked_list = self.data[index]

    if not linked_list:
      return None

    node = linked_list.head

    while node:
      if node.value[0] == key:
        return node.value[1]

      node = node.next

    return None

  def remove(self, key: int):
    """Removes the key-value pair based on the key.
    
    Time Complexity O(1):
      Average Case: O(1) with no collisions.
      Worst Case: O(n) with many collisions.
    """
    index = self.generate_hash(key)
    linked_list = self.data[index]

    if not linked_list:
      raise KeyError
    try:
      node = linked_list.head
    except IndexError:
      raise KeyError
    if node and node.value[0] == key:
      linked_list.delete_head()
      return

    while node:
      if not node.next:
        raise KeyError

      if node.next.value[0] == key:
        node.next = node.next.next
        break

      node = node.next

  def generate_hash(self, key: int) -> int:
    """Generate a hash value (index) based on the key."""
    if key not in range(self.size):
      return key % self.size

    return key
