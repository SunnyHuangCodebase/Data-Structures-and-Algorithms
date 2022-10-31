import pytest

from algorithms.strings import String


class TestStrings:

  @pytest.fixture
  def string(self) -> str:
    return "A mixed case Python string"

  def test_count_vowels(self, string: str):
    assert String.count_vowels(string) == 7
    assert String.count_vowels("lowercase string") == 5
    assert String.count_vowels("UPPERCASE STRING") == 5
    assert String.count_vowels("") == 0
    assert String.count_vowels(None) == 0

  def test_reverse_string(self, string: str):
    assert String.reverse_string(string) == "gnirts nohtyP esac dexim A"
    assert String.reverse_string("singular") == "ralugnis"
    assert String.reverse_string("") == ""
    assert String.reverse_string(None) == ""

  def test_reverse_word_order(self, string: str):
    assert String.reverse_word_order(string) == "string Python case mixed A"
    assert String.reverse_word_order("singular") == "singular"
    assert String.reverse_word_order("") == ""
    assert String.reverse_word_order(None) == ""

  def test_is_rotation(self, string: str):
    assert String.is_rotation(string, "Python stringA mixed case ")
    assert String.is_rotation("AAAAAB", "BAAAAA")
    assert String.is_rotation("ABACAD", "ACADAB")
    assert String.is_rotation("ABACAD", "ADABAC")
    assert String.is_rotation("", "")
    assert String.is_rotation(None, "") == False

  def test_remove_duplicate_characters(self, string: str):
    assert String.remove_duplicate_characters(string) == "A mixedcsPythonrg"
    assert String.remove_duplicate_characters("ABACAD") == "ABCD"
    assert String.remove_duplicate_characters("AaAaA") == "A"
    assert String.remove_duplicate_characters("aAaAa") == "a"
    assert String.remove_duplicate_characters("") == ""
    assert String.remove_duplicate_characters(None) == ""

  def test_most_frequent_character(self, string: str):
    assert String.most_frequent_character(string) == " "
    assert String.most_frequent_character("AAAAAB") == "a"
    assert String.most_frequent_character("ABACAD") == "a"
    assert String.most_frequent_character("AaBBc") == "a"
    with pytest.raises(ValueError):
      assert String.most_frequent_character("") == ""
    with pytest.raises(ValueError):
      assert String.most_frequent_character(None) == ""

  def test_capitalize_words(self, string: str):
    assert String.capitalize_words(string) == "A Mixed Case Python String"
    assert String.capitalize_words("bad    format") == "Bad Format"
    assert String.capitalize_words("  BAD   FORMAT   ") == "Bad Format"
    assert String.capitalize_words(" ") == ""
    assert String.capitalize_words("") == ""
    assert String.capitalize_words(None) == ""

  def test_is_anagram(self):
    assert String.is_anagram("ABCD", "ABCD")
    assert String.is_anagram("ABCD", " ") == False
    assert String.is_anagram("ABCD", "") == False
    assert String.is_anagram("ABCD", None) == False
    assert String.is_anagram("ABCD", "abcd")
    assert String.is_anagram("CABC", "ABCC")
    assert String.is_anagram("three", "ether")
    assert String.is_anagram("", "")

  def test_is_palindrome(self, string: str):
    assert String.is_palindrome(string) == False
    assert String.is_palindrome("ABCDDCBA")
    assert String.is_palindrome("ABCDCBA")
    assert String.is_palindrome("ABCD") == False
    assert String.is_palindrome(" ")
    assert String.is_palindrome("")
    assert String.is_palindrome(None) == False


if __name__ == "__main__":
  pytest.main([__file__, "-vv"])
