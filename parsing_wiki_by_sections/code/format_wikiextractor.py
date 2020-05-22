"""
Convert the output of WikiExtractor into TEAR wiki input format.

WikiExtractor from https://github.com/attardi/wikiextractor, commit 16186e2.
"""

import argparse
import json
from pathlib import Path
import pdb
from collections import defaultdict


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path,
                        help='WikiExtractor output in JSON Lines format.')
    parser.add_argument('output', type=Path,
                        help='Filtered JSON Lines output file.')
    parser.add_argument(
        'filter', type=Path, help='Text file of newline delimited article IDs as whitelist.')
    parser.add_argument('rel_sections', type=Path, default=None,
                        help="Only include relevant sections")
    parser.add_argument('-f', action="store_true",
                        help="Generate frequency of heuristics")
    args = parser.parse_args()

    if args.rel_sections:
        with args.rel_sections.open(encoding="utf8") as rel_sections:
            relevant_sections = set(line.strip()
                                    for line in rel_sections.readlines())

    with args.filter.open(encoding='utf8') as filter_file:
        ids = set(line.strip() for line in filter_file.readlines())

    frequency = defaultdict(int)
    with args.input.open(encoding='utf8') as in_file, \
            args.output.open('w', encoding='utf8') as out_file:
        for line in in_file:

            article = json.loads(line)
            if article['id'] not in ids:
                continue

            print(f'Writing {article["id"]}')
            if args.s:
                final_text = []
                texts = article["text"].split("Section::::")
                for section in texts:
                    section_title = section.split("\n")[0]
                    frequency[section_title] += 1
                    for rel_section in relevant_sections:
                        if rel_section in section_title.lower():
                            section_text = section[len(section_title):]
                            if section_text:
                                final_text.append(section_text)

                article["text"] = " ".join(final_text)
                line = json.dumps(article)

            out_file.write(f"{line}\n")

    if args.f:
        if not args.rel_sections:
            raise ValueError(
                "Cannot generate frequency of heuristics without relevant sections")
        with open("frequency_of_heuristics.json", "w+") as f:
            f.write(json.dumps(frequency))


if __name__ == '__main__':
    main()
