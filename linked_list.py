"""Linked List
    This module defines and implements a Linked List for instructional purposes.
    There is already a standard library for linked lists (collections.deque):
        from collections import deque

    A linked list is a sequence of items.
    A linked list can be singly-linked, doubly-linked, or a cycle.
    Searching a linked list takes O(n) time.
    Accessing, inserting, and deleting takes O(1) time.

    Advantages of a linked list:
    Insertion/Deletion at the start of the list takes O(1) time (O(n) for arrays).

"""
from __future__ import annotations
from typing import Any


class Node:
    """The basic unit of a linked list."""
    value: Any

    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return str(self.value)


class UnidirectionalNode(Node):
    """The basic unit of a singly linked list."""
    value: Any
    next: UnidirectionalNode

    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next


class BidirectionalNode(Node):
    """The basic unit of a doubly linked list."""
    value: Any
    next: BidirectionalNode
    prev: BidirectionalNode

    def __init__(self, value=None, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev


class LinkedList:
    """A linked list contains nodes linked to other nodes.
    A linked list can be traversed in only one direction.
    Head represents the start of a linked list.
    """
    head: Node

    def __repr__(self):
        """Returns all values of a node starting at the head of the list."""
        if not self.head:
            return str([])

        node = self.head
        node_list = [node.value]

        while node and node.next:
            node_list.append(node.next.value)
            node = node.next

        return str(node_list)


class SinglyLinkedList(LinkedList):
    """A singly linked list contains linked nodes in one direction."""
    head: UnidirectionalNode = None
    # The size attribute is only used for the alternative self.is_cycle property.
    # Otherwise, it serves no other purpose.
    size: int = 0

    @property
    def is_cycle(self):
        """Returns whether the linked list is a cycle. Uses tortoise and hare algorithm."""
        slow = fast = self.head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
            if fast == slow:
                return True
        return False

    @property
    def is_cycle_based_on_size(self):
        """Returns whether the linked list is a cycle. Requires size attribute."""
        node = self.head
        for _ in range(self.size):
            node = node.next
        return bool(node)

    def push_left(self, value):
        """Insert node at the start of the linked list.
        Time complexity: O(1)."""
        self.head, self.head.next = UnidirectionalNode(value), self.head
        self.size += 1

    def push_right(self, value):
        """Insert node at the end of the linked list.
        Time complexity: O(n)."""
        node = self.head
        while node.next:
            node = node.next
        node.next = UnidirectionalNode(value)
        self.size += 1

    def pop_left(self):
        """Removes and returns the node at the start of the linked list.
        Time complexity: O(1)."""
        if not self.head:
            return None
        node, self.head = self.head, self.head.next
        self.size -= 1
        return node

    def pop_right(self):
        """Removes and returns the node at the end of the linked list.
        Time complexity: O(n)."""
        node = self.head
        while node.next and node.next.next:
            node = node.next

        # Does not pop the item
        # node, node.next = node.next, None

        # Must set node.next to None before setting the return node
        node.next, node = None, node.next
        self.size -= 1
        return node

    def search_prev_node_value(self, value):
        """Looks up node by its value and returns its previous node.
        Useful when trying to insert or delete nodes."""
        node = self.head
        while node.next and node.next.value != value:
            node = node.next
        return node

    def search_prev_node_position(self, position):
        """Looks up node by its position in linked list and returns its previous node.
        Useful when trying to insert or delete nodes."""

        node = self.head
        for i in range(position):
            if node.next and i+1 < position:
                node = node.next
        return node

    def search_node(self, target):
        """Returns the target node."""
        node = self.head
        while node and node.value != target:
            node = node.next
        return node

    def insert_left_node(self, value, *, target=None, position=None):
        """Insert new node to the left of the first node matching search criteria."""
        new_node = UnidirectionalNode(value)

        if target and position:
            print("Cannot add a node by both target and position.")
            return

        node = self.search_prev_node_value(target) if target is not None\
            else self.search_prev_node_position(position)

        if node.next:
            new_node.next, node.next = node.next, new_node
        else:
            new_node.next, self.head = self.head, new_node
        self.size -= 1

    def insert_right_node(self, value, *, target=None, position=None):
        """Insert new node to the left of the first node matching search criteria."""
        new_node = UnidirectionalNode(value)

        if target and position:
            print("Cannot add a node by both target and position.")
            return

        node = self.search_prev_node_value(target) if target is not None\
            else self.search_prev_node_position(position)

        if node.next:
            new_node.next, node.next.next = node.next.next, new_node
        else:
            new_node.next, node.next = node.next, new_node

        self.size += 1

    def delete_node(self, *, value=None, position=None):
        """Delete a node by its value.
        Time Complexity:
        Best Case: O(1) if deleting at the start.
        Worst Case: O(n) if deleting at the end.
        """
        if value and position:
            print("Cannot add a node by both target and position.")
            return

        node = self.search_prev_node_value(value) if value is not None\
            else self.search_prev_node_position(position)

        node.next = node.next.next
        self.size -= 1


class DoublyLinkedList(LinkedList):
    """A doubly linked list contains linked nodes in two directions. With the addition
    of a prev attribute, inserting and deleting elements at the end of the list has a
    runtime complexity of O(1)."""
    head: BidirectionalNode
    tail: BidirectionalNode
    size: int = 0

    def push_right(self, value):
        """Insert node at the end of the linked list.
        Time complexity: O(1)."""
        node = BidirectionalNode(value)
        self.tail.next, node.prev, self.tail = node, self.tail, node
        self.size += 1

    def pop_right(self):
        """Removes and returns the node at the end of the linked list.
        Time complexity: O(1)."""
        if not self.tail:
            return None
        node, self.tail,  = self.tail, self.tail.prev
        self.tail.next = None
        self.size -= 1
        return node

