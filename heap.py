"""Heap
    This module defines and implements a Heap for instructional purposes.
    There is already a standard library for heaps called heapq.
    
    A heap is a type of binary tree data structure.
    Heap Requirements:
        A root (parent) node.
        Each node can have up to two children (left and right).
        Max Heap: All root values are greater than its children's values.
        Min Heap: All root values are less than its children's values.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto

class Node:
    """The basic unit of a heap."""
    value: int
    left_child: Node
    right_child: Node

    @property
    def is_min_heap_node(self) -> bool:
        """To satisfy a min heap requirement, the root node's value
        must be less than both of its children's values. """
        return self.value < min(self.left_child.value, self.right_child.value)

    @property
    def is_max_heap_node(self) -> bool:
        """To satisfy a max heap requirement, the root node's value
        must be greater than both of its children's values. """
        return self.value > max(self.left_child.value, self.right_child.value)


class Tree:
    """The base structure of a Heap. """
    nodes: list[Node] | list[int]


class HeapType(Enum):
    """Enumerates the Max Heap and Min Heap types."""
    MAX = auto()
    MIN = auto()


@dataclass
class Heap(Tree):
    """A heap is a type of tree with additional rules.
     
    Max Heap: Each root value must be greater than its children's values.
    Min Heap: Each root value must be smaller than its children's values.

    Although a heap can be  visually represented by a tree, it can also 
    be represented by a list. This module uses the list representation.
    """
    type: HeapType
    # size: int = 0
    nodes: list[Node] | list[int] = field(init=False, default_factory=list)

    @property
    def size(self) -> int:
        """Returns heap size."""
        return len(self.nodes)

    @property
    def is_valid_min_heap(self) -> bool:
        """All nodes must have values less than their children's."""
        return all([node.is_min_heap_node for node in self.nodes])

    @property
    def is_valid_max_heap(self) -> bool:
        """All nodes must have values greater than their children's."""
        return all([node.is_max_heap_node for node in self.nodes])

    @property
    def is_valid_heap(self) -> bool:
        """Valid heap check varies depending on the initialized Heap Type."""
        return self.is_valid_max_heap if self.type == HeapType.MAX \
            else self.is_valid_min_heap
    
    def parent_index(self, index):
        """The calculated index of the current node's parent."""
        return (index - 1) // 2

    def left_child_index(self, index):
        """The calculated index of the current node's left child."""
        return 2 * index + 1

    def right_child_index(self, index):
        """The calculated index of the current node's right child."""
        return 2 * index + 2

    def has_parent(self, index):
        """Returns whether the current node has a parent.
        If the parent index is less than 0, no parent exists."""
        return self.parent_index(index) >= 0

    def has_left_child(self, index):
        """Returns whether the current node has a left child.
        If the child index exceeds the heap size, no child exists."""
        return self.left_child_index(index) < self.size

    def has_right_child(self, index):
        """Returns whether the current node has a right child.
        If the child index exceeds the heap size, no child exists."""
        return self.right_child_index(index) < self.size

    def parent(self, index):
        """Returns the parent's value."""
        return self.nodes[self.parent_index(index)]

    def left_child(self, index):
        """Returns the left child's value."""
        return self.nodes[self.left_child_index(index)]

    def right_child(self, index):
        """Returns the right child's value."""
        return self.nodes[self.right_child_index(index)]

    def swap(self, index_1, index_2):
        """Swaps two values in the heap."""
        self.nodes[index_1], self.nodes[index_2] = self.nodes[index_2], self.nodes[index_1]

    def push(self, value):
        """Adds a number to the heap."""
        # Add number to the end (bottom) of the heap.
        self.nodes.append(value)

        # Sort the new value to a valid position.
        self.heapify_up(self.size - 1)

    def pop(self):
        """Retrieve the top number from the heap and reorder the heap.
        Max Heap: Return the largest number.
        Min Heap: Return the smallest number.
        """
        # Swap the top-most and bottom-most heap values.
        self.swap(0, self.size - 1)

        # Return the previously top-most value.
        value = self.nodes.pop()

        # Sort the previously bottom-most value to a valid position.
        self.heapify_down(0)
        return value

    def heapify_up(self, index):
        """Recursively pushes a value towards the top of a heap.
        Max Heap: Push higher values up.
        Min Heap: Push lower values up.
        """
        # If there is no parent, no further reordering necessary.
        if not self.has_parent(index):
            return

        # Move larger numbers upwards in a max heap.
        # Move smaller numbers upwards in a min heap.
        if self.type == HeapType.MAX and self.nodes[index] > self.parent(index)\
        or self.type == HeapType.MIN and self.nodes[index] < self.parent(index):
            # Reorder the current node and its parent if out of order.
            self.swap(index, self.parent_index(index))
            # Push the value up to a valid position.
            self.heapify_up(self.parent_index(index))

    def heapify_down(self, index):
        """Recursively pushes a value toward the bottom of a heap.
        Max Heap: Push lower values down.
        Min Heap: Push higher values down.
        """
        # If there are no children, no further reordering necessary.
        # Left child is added before the right. No left child means no right.
        if not self.has_left_child(index):
            return
       
        # Initialize values for comparison.
        root_value = self.nodes[index]
        left_child = self.left_child(index)
        child_index = self.left_child_index(index)

        # If right child exists, compare to left child.
        if self.has_right_child(index):
            right_child = self.right_child(index)
            # Max Heap: Set child index to the larger child's index.
            # Min Heap: Set child index to the smaller child's index.
            if self.type == HeapType.MAX and right_child > left_child\
            or self.type == HeapType.MIN and right_child < left_child:
                child_index = self.right_child_index(index)

        # Reorder if root and child are out of order
        # Max Heap should have root value > child value
        # Min Heap shoudl have root value < child value
        child_value = self.nodes[child_index]
        if self.type == HeapType.MAX and not root_value > child_value\
        or self.type == HeapType.MIN and not root_value < child_value:      
            self.swap(index, child_index)
            self.heapify_down(child_index)
