class String:

  @staticmethod
  def count_vowels(string: str | None) -> int:
    """Returns the number of vowels in the string.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not string:
      return 0

    vowels: set[str] = {"a", "e", "i", "o", "u"}
    count: int = 0
    for char in string:
      if char.lower() in vowels:
        count += 1
    return count

  @staticmethod
  def reverse_string(string: str | None) -> str:
    """Reverses the characters in a string.

    Time Complexity: O(n^2)
    Space Complexity: O(n)
    """
    if not string:
      return ""

    stack: list[str] = []
    length: int = len(string)

    for i in range(length - 1, -1, -1):
      stack.append(string[i])

    return "".join(stack)

  @staticmethod
  def reverse_word_order(string: str | None):
    """Reverses the word in a string.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not string:
      return ""

    stack: list[str] = []
    current_word: list[str] = []

    for char in string:
      if char == " ":
        stack.append("".join(current_word))
        current_word.clear()

      else:
        current_word.append(char)

    stack.append("".join(current_word))

    reversed_words: list[str] = []
    while stack:
      reversed_words.append(stack.pop())

    return " ".join(reversed_words)

  @staticmethod
  def is_rotation(string1: str | None, string2: str | None) -> bool:
    """Checks if a string is a rotation of another string.
    
    Time Complexity: O(n)
      Worst Case: O(n^2) with many repeating characters.
    Space Complexity: O(1)
    """
    if string1 is None or string2 is None:
      return False

    if string1 == string2:
      return True

    if len(string1) != len(string2):
      return False

    target = string1[0]

    for offset, char in enumerate(string2):
      if char == target and String._is_rotation(string1, string2, offset):
        return True

    return False

  @staticmethod
  def _is_rotation(string1: str | None, string2: str | None, offset: int):
    """Helper method to check if string is a rotation of another string.
    
    Time Complexity: O(n)
    """
    if string1 is None or string2 is None:
      return False

    if string1 == string2:
      return True

    for i, char in enumerate(string1):
      j = (i + offset) % len(string2)
      if char != string2[j]:
        return False

    return True

  @staticmethod
  def remove_duplicate_characters(string: str | None):
    """Removes duplicate characters from a string.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not string:
      return ""

    char_set: set[str] = set()
    characters: list[str] = []
    for char in string:
      if char.lower() not in char_set:
        char_set.add(char.lower())
        characters.append(char)

    return "".join(characters)

  @staticmethod
  def most_frequent_character(string: str | None) -> str:
    """Returns the most commonly occurring character in a string.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not string:
      raise ValueError

    char_frequency: dict[str, int] = {}
    max_frequency: int = 0
    most_common_character = ""

    for char in string:
      count = 1 + char_frequency.get(char.lower(), 0)
      char_frequency[char.lower()] = count

      if count > max_frequency:
        max_frequency = count
        most_common_character = char.lower()

    return most_common_character

  @staticmethod
  def capitalize_words(string: str | None) -> str:
    """Capitalizes first letter of a word and removes extra spaces.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not string:
      return ""

    words: list[str] = []
    current_word: list[str] = []

    for char in string:

      if char == " ":
        if current_word:
          words.append("".join(current_word))
          current_word.clear()
        continue

      if current_word:
        current_word.append(char.lower())
      else:
        current_word.append(char.upper())

    if current_word:
      words.append("".join(current_word))

    return " ".join(words)

  @staticmethod
  def is_anagram(string1: str | None, string2: str | None) -> bool:
    """Checks if two strings contain the same letters.
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if string1 is None or string2 is None:
      return False

    string1 = string1.lower()
    string2 = string2.lower()

    if string1 == string2:
      return True

    if len(string1) != len(string2):
      return False

    char_count: dict[str, int] = {}

    for char in string1:
      char_count[char] = 1 + char_count.get(char, 0)

    for char in string2:
      if char not in char_count:
        return False

      char_count[char] -= 1

      if char_count[char] == 0:
        del char_count[char]

    return len(char_count) == 0

  @staticmethod
  def is_palindrome(string: str | None) -> bool:
    """Checks if a string is the same when read in reverse.
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if string is None:
      return False

    left = 0
    right = len(string) - 1

    while left <= right:
      if string[left] != string[right]:
        return False

      left += 1
      right -= 1

    return True
