import pytest

from data_structures.hashmap import Hashmap


class TestHashmap:

  @pytest.fixture
  def hashmap(self) -> Hashmap:
    return Hashmap(10)

  def test_hashmap(self, hashmap: Hashmap):
    """assert hashmap.is_empty == False
    assert hashmap.to_array() == [0, 1, 2, 3, 4]"""

  def test_hashmap_insert(self, hashmap: Hashmap):
    hashmap.insert(10, "Hello")
    hashmap.insert(20, "World!")
    hashmap.insert(11, "Goodbye")
    hashmap.insert(21, "World...")
    assert hashmap.get(10) == "Hello"
    assert hashmap.get(20) == "World!"

    hashmap.insert(10, "Goodbye")
    assert hashmap.get(10) == "Goodbye"

  def test_hashmap_get(self, hashmap: Hashmap):
    hashmap.insert(10, "Hello")
    hashmap.insert(20, "World!")
    hashmap.insert(11, "Goodbye")
    hashmap.insert(21, "World")

    assert hashmap.get(10) == "Hello"
    assert hashmap.get(20) == "World!"
    assert hashmap.get(11) == "Goodbye"
    assert hashmap.get(21) == "World"
    assert hashmap.get(22) == None

  def test_hashmap_remove_index_head(self, hashmap: Hashmap):
    hashmap.insert(10, "Hello")
    hashmap.remove(10)
    hashmap.insert(10, "Hello")
    hashmap.insert(20, "World")
    hashmap.remove(10)

    assert hashmap.get(10) == None

  def test_hashmap_remove_index_middle_values(self, hashmap: Hashmap):

    hashmap.insert(10, "Hello")
    hashmap.insert(20, "Beautiful")
    hashmap.insert(30, "World")
    hashmap.remove(20)

    assert hashmap.get(10) == "Hello"
    assert hashmap.get(20) == None
    assert hashmap.get(30) == "World"

  def test_hashmap_remove_index_ending_values(self, hashmap: Hashmap):

    hashmap.insert(10, "Hello")
    hashmap.insert(20, "Beautiful")
    hashmap.insert(30, "World")
    hashmap.remove(30)
    assert hashmap.get(10) == "Hello"
    assert hashmap.get(20) == "Beautiful"
    assert hashmap.get(30) == None

  def test_hashmap_remove_empty_index(self, hashmap: Hashmap):
    with pytest.raises(KeyError):
      hashmap.remove(10)
    hashmap.insert(10, "Hello")
    hashmap.remove(10)
    with pytest.raises(KeyError):
      hashmap.remove(10)


if __name__ == "__main__":
  pytest.main([__file__])
