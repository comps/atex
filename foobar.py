#!/usr/bin/python3

import sys
from .lib import test

def main():
    print(f"running foobar!: {sys.argv}")
    test.blah()

print("importing!")
