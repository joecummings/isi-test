import argparse
import json
import csv

def findall_events_in_range(events, lb, ub):
    ret_e = []

    for e in events:
        if e["span_start"] > ub:
            continue
        if e["span_start"] > lb and e["span_end"] < ub:
            ret_e.append(e["text"])
    
    return ret_e

def create_csv(tbd, matres, output):
    tbd_sentences = tbd["sentences"]
    tbd_events = tbd["events"]
    matres_sentences = matres["sentences"]
    matres_events = matres["events"]

    tsv = open("/Users/jcummings/Desktop/projects/LESTAT/test/duration/data/MCTACO-origin/dataset/dev_3783.tsv")
    read_tsv = csv.reader(tsv, delimiter="\t")

    durations = []
    for row in read_tsv:
        if row[4] == "Event Duration":
            durations.append(row)

    combined = []
    for sent in tbd_sentences:
        sent_text = sent["text"].replace(" .", "?")
        tbd_es = findall_events_in_range(tbd_events, sent["span_start"], sent["span_end"])
        matres_es = findall_events_in_range(matres_events, sent["span_start"], sent["span_end"])
        
        good,bad = [],[]
        for entry in durations:
            if entry[1] == sent_text:
                if entry[3] == "no":
                    bad.append(entry[2])
                elif entry[3] == "yes":
                    good.append(entry[2])

        row = [sent_text, tbd_es, matres_es, [], good, bad]
        combined.append(row)

    with open(output, "w+", newline='') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(["sentence", "tbd_events", "matres_events", "oneie_events", "possible_durations", "not_possible_durations"])
        writer.writerows(combined)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('-i_tbd', help='input TBD doc')
    p.add_argument('-i_matres', help='input MATRES doc')
    p.add_argument('-o', help='output doc')
    args = p.parse_args()

    with open(args.i_tbd) as file:
        tbd = json.load(file)

    with open(args.i_matres) as file:
        matres = json.load(file)

    create_csv(tbd[0], matres[0], args.o)

    return

if __name__ == '__main__':
    main()