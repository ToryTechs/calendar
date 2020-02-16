#!/usr/bin/env python3

import argparse
from datetime import datetime
import json
import ics_converter
import scrape
from ics import Calendar
import os

#import create_ics
#import store
#import sys

#def run():
#    test_mode = "--fake-data" in sys.argv
#
#    event_data = scrape.get_all_calendar_data()
#
#    if test_mode:
#        events = store.transform(store.fakeData())
#    else:
#        events = store.transform(event_data)
#
#    create_ics.make(filename, events)

def try_convert_date_from_str(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except:
        return None


def output_calendar_ics(calendar: Calendar, filename: str):
    if filename is None:
        print(str(calendar))
    else:
        with open(filename, "w") as ics_file:
            ics_file.writelines(calendar)


def convert_parliament_website_event_data_to_ics_events(result_object: {}):
    if result_object["Results"]["HasEvents"] is True:
        return ics_converter.parse_parliament_groupped_events(result_object["Results"]["Groupings"])
    else:
        return []


def create_ics_calendar_for_events(ics_events: []):
    calendar = ics_converter.add_ics_events_to_calendar(ics_events)
    return calendar


def run():
    argParser = argparse.ArgumentParser()
    # load data from a json file stored locally
    argParser.add_argument("--inputfile", help="Use data stored in a json file", type=argparse.FileType("r"), required=False)
    # scrape and load the events of a specific day on the Parliament website
    argParser.add_argument("--singledate", help="Scrape calendar events of a specific date in the format of yyyy-mm-dd from the Parliament website", required=False)
    # the filename for the ics file.  if not set, print to the screen.
    argParser.add_argument("--outputfile", help="Save the calendar as an ICS file (or to STDOUT if not specified)", required=False)
    # The House - Commons or Lords
    argParser.add_argument("--house", help="The House (default: Commons) - needed in conjunction with --singledate", required=False, default="Commons")
    # export the json for caching
    argParser.add_argument("--jsondump", help="Dump the json file instead of exporting an ics file", action="store_true", required=False)
    # load data from json files stored in a local directory 
    argParser.add_argument("--inputdirectory", help="Use data stored in json files inside a directory", required=False)

    args = argParser.parse_args()

    if args.inputfile is not None:
        # load the json from a local file and export an ics file
        parliament_response_obj = json.load(args.inputfile)
        ics_events = convert_parliament_website_event_data_to_ics_events(parliament_response_obj)
        ics_calendar = create_ics_calendar_for_events(ics_events)
        output_calendar_ics(ics_calendar, args.outputfile)
    elif args.inputdirectory is not None:
        # load all json files in a directory and its sub directories
        all_events_from_json_files = []
        for (root, dirs, files) in os.walk(args.inputdirectory, topdown=True):
            for filename in files:
                if filename.endswith(".json"):
                    json_filename = os.path.join(root, filename)
                    parliament_response_obj = json.load(open(json_filename, 'r'))
                    print(json_filename)
                    ics_events = convert_parliament_website_event_data_to_ics_events(parliament_response_obj)
                    all_events_from_json_files.extend(ics_events)
        ics_calendar = create_ics_calendar_for_events(all_events_from_json_files)
        output_calendar_ics(ics_calendar, args.outputfile)
    elif args.singledate is not None:
        # for scraping, the House needs to be specified
        if args.house not in ["Commons", "Lords"]:
            print("Invalid House")
            return
        # cannot proceed if the date cannot be correctly parsed
        date = try_convert_date_from_str(args.singledate)
        if date is not None:
            # scrape, parse and export an ics file
            parliament_response_obj = scrape.get_parliament_events_data(date, args.house)
            if args.jsondump is True:
                if args.outputfile is not None:
                    with open(args.outputfile, "w") as json_file:
                        json_file.write(json.dumps(parliament_response_obj)) 
                else:
                    print(json.dumps(parliament_response_obj))
            else:
                ics_events = convert_parliament_website_event_data_to_ics_events(parliament_response_obj)
                ics_calendar = create_ics_calendar_for_events(ics_events)
                output_calendar_ics(ics_calendar, args.outputfile)
        else:
            print("The date format is invalid.  Please use --help.")
    else:
        argParser.print_help()


if __name__ == '__main__':
    run()
