import json
import argparse
from pathlib import Path

def main(args):
    pass
    

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-i", type=Path, help="File of Wiki articles, in JSON Lines format")
    args = p.parse_args()
    main(args)