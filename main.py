#!/usr/bin/env python3

import scrape
import create_ics
import store

def run():
    event_data = scrape.get_all_calendar_data()
    events = store.transform(event_data)
    create_ice.make(filename, events)

if __name__ == '__main__':
    run()
