import pytest

from data_structures.trie import ArrayTrieNode, DictTrieNode, Trie, TrieFactory


class TestTrie:

  @pytest.fixture
  def new_trie(self) -> Trie[DictTrieNode]:
    return TrieFactory.create_dict_trie()

  @pytest.fixture
  def trie(self) -> Trie[DictTrieNode]:
    trie = TrieFactory.create_dict_trie()
    trie.insert("Hello")
    trie.insert("World")
    trie.insert("Help")
    trie.insert("Helping")
    trie.insert("Helix")
    return trie

  @pytest.fixture
  def array_trie(self) -> Trie[ArrayTrieNode]:
    trie = TrieFactory.create_array_trie()
    trie.insert("Hello")
    trie.insert("World")
    trie.insert("Help")
    trie.insert("Helping")
    trie.insert("Helix")
    return trie

  def test_trie(self, trie: Trie[DictTrieNode],
                array_trie: Trie[ArrayTrieNode]):
    assert trie.root.value == " "
    assert array_trie.root.value == " "

  def test_trie_lookup(self, trie: Trie[DictTrieNode],
                       array_trie: Trie[ArrayTrieNode]):

    for t in (trie, array_trie):
      assert t.lookup("Hello")
      assert t.lookup("World")
      assert t.lookup("Help")
      assert t.lookup("Helping")
      assert t.lookup("Helix")
      assert t.lookup("") == False
      assert t.lookup("H") == False
      assert t.lookup("He") == False
      assert t.lookup("Word") == False
      assert t.lookup("Worldly") == False

  def test_trie_insert(self, new_trie: Trie[DictTrieNode],
                       array_trie: Trie[ArrayTrieNode]):

    assert new_trie.lookup("Hello") == False
    new_trie.insert("Hello")
    assert new_trie.lookup("Hello")

    for t in (new_trie, array_trie):
      with pytest.raises(Exception):
        t.insert("!")

  def test_trie_delete(self, trie: Trie[DictTrieNode],
                       array_trie: Trie[ArrayTrieNode]):
    for t in (trie, array_trie):
      assert t.lookup("Help")
      t.delete("Help")
      assert t.lookup("Help") == False
      assert t.lookup("Helping")
      t.insert("Help")
      t.delete("Helping")
      assert t.lookup("Help")
      assert t.lookup("Helping") == False
      assert t.delete("") == None
      assert t.delete("Nonexistent") == None

  def test_trie_autocomplete(self, trie: Trie[DictTrieNode],
                             array_trie: Trie[ArrayTrieNode]):
    for t in (trie, array_trie):
      assert set(t.auto_complete("")) == {
          "hello", "help", "helping", "helix", "world"
      }
      assert set(t.auto_complete("h")) == {"hello", "help", "helping", "helix"}
      assert set(t.auto_complete("help")) == {"help", "helping"}
      assert t.auto_complete("helix") == ["helix"]
      assert t.auto_complete("nonexistent") == []


if __name__ == "__main__":
  pytest.main([__file__, "-vv"])
