import json
from collections import Counter, defaultdict
from format_wikiextractor import RELEVANT_SECTIONS
from pprint import pprint

def main():

    with open("frequency_of_heuristics.json") as f:
        freq = json.load(f)

    # for section in RELEVANT_SECTIONS:
    #     print(freq.get(section))

    collapsed_freq = defaultdict(int)
    total_count = 0
    for key, count in freq.items():
        for section in RELEVANT_SECTIONS:
            if section in key.lower():
                collapsed_freq[section] += count
                total_count += count

    c = Counter(freq)
    pprint(c.most_common(20))

    # print(len(list(freq.keys())))
    # print(total_count)
    print(total_count/ len(list(freq.keys())))
    pprint(collapsed_freq)

if __name__ == "__main__":
    main()