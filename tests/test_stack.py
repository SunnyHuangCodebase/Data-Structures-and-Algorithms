import pytest

from data_structures.stack import Stack


class TestStack:

  @pytest.fixture
  def stack(self) -> Stack[int]:
    return Stack([0, 1, 2, 3, 4])

  @pytest.fixture
  def empty_stack(self) -> Stack[int]:
    return Stack([])

  def test_stack(self, stack: Stack[int]):
    assert stack.is_empty == False
    assert stack.to_array() == [0, 1, 2, 3, 4]

  def test_stack_push(self, stack: Stack[int]):
    assert stack.peek() == 4
    stack.push(5)
    assert stack.peek() == 5

  def test_stack_pop(self, stack: Stack[int]):
    assert stack.peek() == 4
    stack.pop()
    assert stack.peek() == 3

  def test_empty_stack_array(self, empty_stack: Stack[int]):
    assert empty_stack.is_empty == True
    assert empty_stack.to_array() == []

  def test_empty_stack_push(self, empty_stack: Stack[int]):
    assert empty_stack.peek() == None
    empty_stack.push(1)
    assert empty_stack.peek() == 1

  def test_empty_stack_pop(self, empty_stack: Stack[int]):
    assert empty_stack.peek() == None
    assert empty_stack.pop() == None


if __name__ == "__main__":
  pytest.main([__file__])
