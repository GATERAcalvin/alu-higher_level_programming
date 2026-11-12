#!/usr/bin/python3
"""Defines a class Square with a private size."""


class Square:
    """A square defined by its size."""

    def __init__(self, size):
        """Initialize a square.

        Args:
            size: the size of the square (not validated).
        """
        self.__size = size
