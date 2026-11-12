#!/usr/bin/python3
"""Solve the N queens problem and print every solution."""
import sys


def solve(n, row, cols, solution, solutions):
    """Place queens row by row, backtracking when a queen is attacked.

    Args:
        n (int): the size of the board.
        row (int): the row to fill next.
        cols (list): the column of the queen placed in each earlier row.
        solution (list): placed queens as [row, column] pairs.
        solutions (list): collects every complete solution.
    """
    if row == n:
        solutions.append(solution[:])
        return
    for col in range(n):
        safe = True
        for r, c in enumerate(cols):
            if c == col or abs(c - col) == row - r:
                safe = False
                break
        if safe:
            cols.append(col)
            solution.append([row, col])
            solve(n, row + 1, cols, solution, solutions)
            solution.pop()
            cols.pop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: nqueens N")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("N must be a number")
        sys.exit(1)
    if n < 4:
        print("N must be at least 4")
        sys.exit(1)
    solutions = []
    solve(n, 0, [], [], solutions)
    for s in solutions:
        print(s)
