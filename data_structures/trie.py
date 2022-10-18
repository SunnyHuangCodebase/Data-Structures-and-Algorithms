"""A trie is a tree containing nodes representing units of a larger sequence.
  Iterating through a trie in DFS order returns a subsequence (prefix) of a larger sequence.
  For tries of words, each node may have up to 26 children (one for each letter of the alphabet).

  This Trie implementation is for instructional purposes and for words.

  Tries also go by the names: digital trees or prefix trees.
  A radix tree is a compressed trie where nodes with a single child node are merged into one.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T", "ArrayTrieNode", "DictTrieNode")


class TrieNode(ABC, Generic[T]):
  """A Trie Node is a unit of a Trie, a larger data structure represented by a sequence of nodes.
  
  Words are a common usage of tries.
  Each node has a letter value and up to 26 children (one for each letter of the alphabet).
  DFS traversal through a trie yields a sequence of letters, which can form words.
  If the Trie's is_end_of_word property is True, terminating the sequence yields a valid word.
  
  If the TrieNode has children, it does not have to be terminated even if it is the end of the word.
  For example, the following Trie:
    T -> R -> E -> E (end_word = True) -> S (end_word = True)
    can yield either TREE or TREES
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
  """A Trie node that uses a dictionary to represent its children."""
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
    """Creates and returns a child node."""
    self._validate_letter(character)
    child = DictTrieNode(character)
    self.children[character] = child
    return child


class ArrayTrieNode(TrieNode["ArrayTrieNode"]):
  """A Trie node that uses an array to represent its children."""
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
    """Creates and returns a child node."""
    child = ArrayTrieNode(character)
    self.children[index] = child
    return child

  def _letter_index(self, character: str):
    """Returns an integer index of a letter based on its Unicode number."""
    self._validate_letter(character)
    index = ord(character) - ord("a")
    return index


class Trie(Generic[T]):
  """Trie is a word retrieval tree containing TrieNodes representing alphabet characters.
  Each node may contain up to 26 children (one for each letter).
  DFS traversal of the trie will produce a prefix of a word.

  A node represents a letter and can have up to 26 children (for each letter).
  """

  root: T

  def __init__(self, root: T) -> None:
    self.root = root

  def lookup(self, word: str):
    """
    Time Complexity: O(n) -> O(1), where n is the length of a word.
    Because words have a finite length and are , the time complexity can be rounded to O(1).
    """
    node: T | None = self.root
    for character in word.lower():
      node = node.get_child(character)    # type: ignore

      if not node:
        return False

    return node.is_end_of_word    # type: ignore

  def insert(self, word: str):
    """
    Time Complexity: O(n)/O(1), where n is the length of a word.
    Because words have a finite length, the time complexity can be rounded to O(1).
    """
    node = self.root

    for character in word.lower():
      node = node.insert_child(character)

    node.is_end_of_word = True

  def delete_word(self, word: str):
    """
    Time Complexity: O(n)/O(1), where n is the length of a word.
    Because words have a finite length, the time complexity can be rounded to O(1).
    """
    if not word:
      return

    self._delete_word(self.root, word.lower(), 0)

  def _delete_word(self, node: T, word: str, index: int):
    if index == len(word):
      node.is_end_of_word = False
      return

    character = word[index]
    child = node.get_child(character)

    if not child:
      return

    self._delete_word(child, word, index + 1)
    if not child.has_children() and not child.is_end_of_word:
      node.delete_child(character)

  def auto_complete(self, word: str) -> list[str]:
    letters: list[str] = list(word)
    matches: list[str] = []

    node = self.get_last_node(word)

    if not node:
      return matches

    self._auto_complete(node, letters, matches)
    return matches

  def get_last_node(self, word: str) -> T | None:
    node: T | None = self.root

    for letter in word:

      if not node:
        return None

      node = node.get_child(letter)

    return node

  def _auto_complete(self, node: T, letters: list[str], matches: list[str]):
    """"""

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
