#!/usr/bin/python3
def roman_to_int(roman_string):
    if not isinstance(roman_string, str) or not roman_string:
        return 0
    values = {"I": 1, "V": 5, "X": 10, "L": 50,
              "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, c in enumerate(roman_string):
        if c not in values:
            return 0
        value = values[c]
        nxt = 0
        if i + 1 < len(roman_string):
            nxt = values.get(roman_string[i + 1], 0)
        if value < nxt:
            total -= value
        else:
            total += value
    return total
