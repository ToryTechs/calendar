#!/usr/bin/env python3

import scrape
import create_ics
import store
import sys

def run():
    test_mode = "--fake-data" in sys.argv

    event_data = scrape.get_all_calendar_data()

    if test_mode:
        events = store.transform(store.fakeData())
    else:
        events = store.transform(event_data)

    create_ics.make(filename, events)

if __name__ == '__main__':
    run()
