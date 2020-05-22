import json
from pathlib import Path
import argparse
import random

DATA_DIR = Path("../data")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("-i", help="input file")
    p.add_argument("-o", help="output file")
    p.add_argument("-m", metavar="mode", choices=["one", "many"])

    args = p.parse_args()

    random.seed(123)

    with open(args.i) as in_file:
        with open(args.o, "w+") as out_file:
            if args.m == "many":
                for line in in_file:
                    mock_id = random.randint(0,1000000)
                    mock_wiki_entry = {"id": str(mock_id), "url": "", "title": "", "text": line}
                    out_file.write(f"{json.dumps(mock_wiki_entry)}\n")
            else: # accounts for mode=one
                mock_id = random.randint(0,1000000)
                mock_wiki_entry = {"id": str(mock_id), "url": "", "title": "", "text": ""}
                text = ""
                for line in in_file:
                    t = line.replace('"', "")
                    t = t.replace("?\n", ". ")
                    text += t
                mock_wiki_entry["text"] = text
                out_file.write(json.dumps(mock_wiki_entry))

    return

if __name__ == "__main__":
    main()