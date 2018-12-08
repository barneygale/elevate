#!/usr/bin/env python3
import os
import sys
import argparse
from elevate import elevate


def is_root():
    if sys.platform.startswith("win"):
        from ctypes import windll
        return bool(windll.shell32.IsUserAnAdmin())
    else:
        return os.getuid() == 0


parser = argparse.ArgumentParser()
parser.add_argument('--sudo', action='store_true')
parser.add_argument('file')
# sudo'd process falls over here due to `--_` options?
print(sys.argv)
args = parser.parse_args()

print("before: ", os.getcwd())
print("before: ", is_root())

if args.sudo:
    elevate()
file = args.file  # sys.argv[1]

print("after:  ", os.getcwd())
print("after:  ", is_root())
print(file)
print(os.getcwd())
print(open(file, "r").readline())

# should print: False True True and a line
