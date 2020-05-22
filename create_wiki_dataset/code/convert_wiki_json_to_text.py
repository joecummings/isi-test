import argparse
import json
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--json_file", type=Path)
    p.add_argument("--doc_output_dir", type=Path)
    args = p.parse_args()

    write_count = 0
    with open(args.json_file, "r") as in_file:
        for line in in_file:
            document = json.loads(line)
            with open(args.doc_output_dir / f"{document['id']}.txt", "w") as out_file:
                out_file.write(document["text"])
            write_count += 1
    print(f"Wrote {write_count} files to {args.doc_output_dir}")

if __name__ == "__main__":
    main()