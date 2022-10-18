"""A trie is a retrieval tree containing nodes that represent units of larger sequences.
  DFS traversal of a trie produces a stack of nodes whose values make up a larger sequence.
  Upon reaching a terminal node, the current stack yields a full sequence.
  
  Example of word autocomplete implemented with a trie:
    The trie contains nodes with a letter value and up to 26 children (one for each letter).
    A node representing the last letter of a word is marked as a terminal node.
    Traversing past a terminal node with children will yield larger words.
    A single sequence can contain multiple words with a common prefix.
    BATCHES can terminate at nodes T, H, or S, yielding BAT, BATCH, or BATCHES, respectively.

  Tries also go by the names: digital trees or prefix trees.
  A radix tree is a compressed trie where nodes with a single child node are merged into one.

  This Trie implementation is for instructional purposes.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T", "ArrayTrieNode", "DictTrieNode")


class TrieNode(ABC, Generic[T]):
  """An abstract base class of a Trie's basic unit.

  Attributes:
    value: A string letter.
    children: A list/dictionary of next-in-sequence TrieNodes mapped to an index or letter.
    _is_end_of_word: A boolean indicating if the sequence is valid when terminated at this node.

  """
  value: str
  children: list[T | None] | dict[str, T]
  _is_end_of_word: bool

  def __init__(self, letter: str) -> None:
    self.value = letter
    self.is_end_of_word = False

  @property
  def is_end_of_word(self) -> bool:
    """Returns True if the current and preceding nodes in sequence is a valid word."""
    return self._is_end_of_word

  @is_end_of_word.setter
  def is_end_of_word(self, value: bool):
    """Sets the current node to a valid/invalid end of word sequence."""
    self._is_end_of_word = value

  def has_children(self) -> bool:
    """Returns whether the node has children."""
    return any(self.children)

  @abstractmethod
  def get_child(self, character: str) -> T | None:
    """Returns the child node of the current character."""

  @abstractmethod
  def get_children(self) -> list[T]:
    """Returns all of a node's children."""

  @abstractmethod
  def insert_child(self, character: str) -> T:
    """Returns a child node of the specified character. Creates child if it doesn't exist."""

  @abstractmethod
  def delete_child(self, character: str):
    """Deletes a child node of the specified character."""

  def _validate_letter(self, character: str):
    if ord(character) - ord("a") not in range(26):
      raise Exception("Invalid character")


class DictTrieNode(TrieNode["DictTrieNode"]):
  """A Trie node implementation with children nodes mapped to their letter in a dictionary."""
  value: str
  children: dict[str, DictTrieNode]
  _is_end_of_word: bool

  def __init__(self, letter: str):
    super().__init__(letter)
    self.children = {}

  def get_child(self, character: str) -> DictTrieNode | None:
    try:
      return self.children[character]
    except KeyError:
      return None

  def get_children(self) -> list[DictTrieNode]:
    return list(self.children.values())

  def insert_child(self, character: str) -> DictTrieNode:

    return self.get_child(character) or self._create_child(character)

  def delete_child(self, character: str):
    print(self.children)
    del self.children[character]

  def _create_child(self, character: str) -> DictTrieNode:
    """Validates and creates a child node, then returns it."""
    self._validate_letter(character)
    child = DictTrieNode(character)
    self.children[character] = child
    return child


class ArrayTrieNode(TrieNode["ArrayTrieNode"]):
  """A Trie node implementation with indexed nodes in an array."""
  CHARSET_SIZE = 26
  value: str
  children: list[ArrayTrieNode | None]
  _is_end_of_word: bool

  def __init__(self, letter: str):
    super().__init__(letter)
    self.children = [None] * self.CHARSET_SIZE

  def get_child(self, character: str) -> ArrayTrieNode | None:
    index = self._letter_index(character)
    return self.children[index]

  def get_children(self) -> list[ArrayTrieNode]:
    return [child for child in self.children if child]

  def insert_child(self, character: str) -> ArrayTrieNode:
    index = self._letter_index(character)
    return self.get_child(character) or self._create_child(index, character)

  def delete_child(self, character: str):
    index = self._letter_index(character)
    self.children[index] = None

  def _create_child(self, index: int, character: str) -> ArrayTrieNode:
    """Creates a child node, then returns it."""
    child = ArrayTrieNode(character)
    self.children[index] = child
    return child

  def _letter_index(self, character: str):
    """Returns an integer index of a letter based on its Unicode number, if it is valid."""
    self._validate_letter(character)
    index = ord(character) - ord("a")
    return index


class Trie(Generic[T]):
  """A Trie implementation for word retrieval and autocomplete.
  
  *Lookup, insert, and delete operations all take O(n) time, where n is the word length.
  Since words are short, the time complexity can be rounded down to O(1) (constant time).
  """

  root: T

  def __init__(self, root: T) -> None:
    self.root = root

  def lookup(self, word: str):
    """Returns whether a valid word was found after iterating through the trie.

    Time Complexity: O(n) / O(1)*
    """
    node: T | None = self.root
    for character in word.lower():
      node = node.get_child(character)    # type: ignore

      if not node:
        return False

    return node.is_end_of_word    # type: ignore

  def insert(self, word: str):
    """Inserts a word into the trie, creating additional nodes if necessary.
    
    Time Complexity: O(n) / O(1)*
    """
    node = self.root

    for character in word.lower():
      node = node.insert_child(character)

    node.is_end_of_word = True

  def delete(self, word: str):
    """Removes a word from the trie, deleting nodes and unmarking terminal nodes if necessary.

    Time Complexity: O(n) / O(1)*
    """
    if not word:
      return

    self._delete(self.root, word.lower(), 0)

  def _delete(self, node: T, word: str, index: int):
    """Recursive helper method that deletes letters from the trie and unmarks terminal nodes."""
    if index == len(word):
      node.is_end_of_word = False
      return

    character = word[index]
    child = node.get_child(character)

    if not child:
      return

    self._delete(child, word, index + 1)
    if not child.has_children() and not child.is_end_of_word:
      node.delete_child(character)

  def auto_complete(self, prefix: str) -> list[str]:
    """Returns all possible words that begin with a prefix string."""
    letters: list[str] = list(prefix)
    matches: list[str] = []

    node = self._get_last_node(prefix)

    if not node:
      return matches

    self._auto_complete(node, letters, matches)
    return matches

  def _get_last_node(self, prefix: str) -> T | None:
    """A helper method that returns the last node of a prefix string."""
    node: T | None = self.root

    for letter in prefix:

      if not node:
        return None

      node = node.get_child(letter)

    return node

  def _auto_complete(self, node: T, letters: list[str], matches: list[str]):
    """A recursive helper method to generate all possible words for autocompletion."""

    if node.is_end_of_word:
      matches.append("".join(letters))

    for child in node.get_children():
      letters.append(child.value)
      self._auto_complete(child, letters, matches)    # type: ignore
      letters.pop()


class TrieFactory:

  @staticmethod
  def create_dict_trie() -> Trie[DictTrieNode]:
    """Create Trie with DictTrieNode"""
    return Trie(DictTrieNode(" "))

  @staticmethod
  def create_array_trie() -> Trie[ArrayTrieNode]:
    """Create Trie with ArrayTrieNode"""
    return Trie(ArrayTrieNode(" "))
