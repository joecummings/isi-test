import csv
import xml.etree.ElementTree as ET
from datetime import timedelta
from pathlib import Path
from statistics import mean, median

import matplotlib.pyplot as plt
import metomi.isodatetime.parsers as parse
import numpy as np
from nltk.stem import WordNetLemmatizer

DATA_DIR = Path("../data")


def collect_event_bounds(doc):
    lemm = WordNetLemmatizer()
    
    root = doc.getroot()

    events = {}
    for event in root.findall(".//EVENT"):
        lower_bound = event.attrib.get("lowerBoundDuration")
        upper_bound = event.attrib.get("upperBoundDuration")
        if lower_bound != "NULL" and lower_bound and upper_bound != "NULL" and upper_bound and event.text:
            lemm_event_text = lemm.lemmatize(event.text, "v")
            if lemm_event_text in events.keys():
                curr_lower_bound = events[lemm_event_text]["lower_bound_duration"]
                temp_lower_bound = parse.DurationParser().parse(lower_bound).get_seconds()
                if curr_lower_bound - temp_lower_bound:
                    events[lemm_event_text]["lower_bound_duration"] = temp_lower_bound
                
                curr_upper_bound = events[lemm_event_text]["upper_bound_duration"]
                temp_upper_bound = parse.DurationParser().parse(upper_bound).get_seconds()
                if temp_upper_bound - curr_upper_bound:
                    events[lemm_event_text]["upper_bound_duration"] = temp_upper_bound
            else:
                lower = parse.DurationParser().parse(lower_bound).get_seconds()
                upper = parse.DurationParser().parse(upper_bound).get_seconds()
                if upper < lower:
                    print(f"Skipping invalid negative duration: {event.text}")
                    print(f"* Lower bound ISO {lower_bound}, lower bound seconds {lower}")
                    print(f"* Upper bound ISO {upper_bound}, upper bound seconds {upper}")
                    continue
                events[lemm_event_text] = {
                    "lower_bound_duration": lower,
                    "upper_bound_duration": upper
                }            
    
    return events

def main():

    total_events = {}
    for xml_file in Path(DATA_DIR / "annotations").glob("./*"):
        annotated_file_tree = ET.parse(xml_file)
        event_duration_bounds = collect_event_bounds(annotated_file_tree)
        total_events.update(event_duration_bounds)

    diffs = np.array(sorted([y["upper_bound_duration"] - y["lower_bound_duration"] for x,y in total_events.items()]))

    out_file = open("timeml_duration_bounds.csv", "w")
    csv_writer = csv.writer(out_file)
    csv_writer.writerow(["event", "lower_bound_duration", "upper_bound_duration"])

    for k,v in total_events.items():
        csv_writer.writerow([k,v["lower_bound_duration"], v["upper_bound_duration"]])
    
    # print([(x,y["upper_bound_duration"]) for x,y in total_events.items() if y["upper_bound_duration"] - y["lower_bound_duration"]])
    
    # max_ = ("", 0.)
    # for event in total_events:
    #     if total_events[event]["upper_bound_duration"] - total_events[event]["lower_bound_duration"] > max_[1]:
    #         max_ = (event, total_events[event]["upper_bound_duration"] - total_events[event]["lower_bound_duration"])

    # print(max_)

    print(len(diffs))
    print(mean(diffs))
    print(median(diffs))

    
    return

    

if __name__ == "__main__":
    main()
