import sys

def in_venv():
    if sys.prefix != sys.base_prefix:
        print("in virtual env")
    else:
        print("NOT in virtual env")

in_venv()