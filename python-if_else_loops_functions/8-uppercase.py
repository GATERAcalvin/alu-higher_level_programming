#!/usr/bin/python3
def uppercase(str):
    for c in str:
        o = ord(c)
        print("{}".format(chr(o - 32 if 97 <= o <= 122 else o)), end="")
    print("")
