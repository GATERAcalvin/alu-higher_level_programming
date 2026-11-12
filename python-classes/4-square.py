#!/usr/bin/python3
"""Defines a class Square with a size property."""


class Square:
    """A square defined by its size."""

    def __init__(self, size=0):
        """Initialize a square.

        Args:
            size (int): the size of the square.
        """
        self.size = size

    @property
    def size(self):
        """int: the size of the square."""
        return self.__size

    @size.setter
    def size(self, value):
        """Set the size of the square.

        Raises:
            TypeError: if value is not an integer.
            ValueError: if value is less than 0.
        """
        if not isinstance(value, int):
            raise TypeError("size must be an integer")
        if value < 0:
            raise ValueError("size must be >= 0")
        self.__size = value

    def area(self):
        """Return the area of the square."""
        return self.__size ** 2
