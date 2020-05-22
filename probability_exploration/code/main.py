"""
Script to build conditional probabilities based on events and their relations

Does not take into account any extra context
TODO: filter out reporting events
"""

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import nltk

REPORTING_LEMMAS = {
    'announce',
    'answer',  # Not in TimeBank
    'assert',
    'cite'
    'claim',
    'declare',
    'deny',
    'disclose',
    'explain',  # Not in TimeBank
    'express',
    'mention',
    'reply',
    'report',
    'respond',
    'reveal',  # Not in TimeBank
    'say',
    'speak',  # Not in TimeBank
    'state',
    'tell',
}

def dependent_probabilities(events_to_ids, relations, conf):
    """
    p(next-event-word | event-word)
    """

    probabilities = defaultdict(lambda: defaultdict(float))
    for relation in relations:
        event1 = events_to_ids[relation["event1_id"]]
        event2 = events_to_ids[relation["event2_id"]]

        # filter reporting
        if event1 == "" or event2 == "":
            continue

        probabilities[event1][event2] += 1

    return probabilities

def add_to_dict(a, b):
    for i in a.keys():
        if i in b.keys():
            b[i] += a[i]
        else:
            b[i] = a[i]
    return b

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, default="all.json")
    p.add_argument("--output", type=Path, default="rel_probabilities.json")
    p.add_argument("--conf", type=float, default=0.75)
    # p.add_argument("--dependent", action="store_true", default=True)
    p.add_argument("--lemm", action="store_true")
    p.add_argument("--filter-reporting", action="store_true")
    args = p.parse_args()

    with open(args.input, encoding="utf-8") as file:
        tear_output = json.load(file)

    events = defaultdict(float)
    lemm = nltk.stem.wordnet.WordNetLemmatizer()

    relations = [doc["relations"] for doc in tear_output]
    events_to_ids = defaultdict(str)
    for doc in tear_output:
        temp_events = defaultdict(float)
        for event in doc["events"]:
            text = event["text"].lower()
            if args.filter_reporting:
                temp = lemm.lemmatize(text, "v")
                if temp in REPORTING_LEMMAS:
                    continue
            if args.lemm:
                text = lemm.lemmatize(text, "v")
            events_to_ids[event["event_id"]] = text
            temp_events[text] = 1.
        events = add_to_dict(temp_events, events)
    
    num_docs = len(tear_output)
    events.update((x, y/num_docs) for x, y in events.items()) 
    # p(event-word | IED doc)
    with open("event_probabilitiesl.json", "w+") as file:
        json.dump(events, file)

    def good_confidences(x): return True if x.get(
        "confidence") >= args.conf else False
    only_good_relations = sum(
        [list(filter(good_confidences, doc)) for doc in relations], [])

    probabilities = dependent_probabilities(events_to_ids, only_good_relations, args.conf)

    for event in probabilities:
        denom = len(probabilities[event].keys())
        for event2 in probabilities[event]:
            probabilities[event][event2] = min(1., probabilities[event][event2] / denom)

    with open(args.output, "w+") as file:
        json.dump(probabilities, file)


if __name__ == "__main__":
    main()
