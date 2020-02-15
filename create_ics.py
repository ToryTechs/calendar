#!/usr/bin/env python3

from ics import Calendar, Event

def make(path, events):
    c = Calendar()
    for event in events:
        e = Event()
        e.name = event.name
        e.begin = event.begin
        c.events.add(e)

    with(path, 'w') as f:
        f.writelines(c)

def run():
    c = Calendar()

    e = Event()
    e.name = "Parliamentary calendar test event"
    e.begin = '2020-02-15 16:00:00'

    c.events.add(e)

    e = Event()
    e.name = "A second test event"
    e.begin = '2020-02-15 16:30:00'

    c.events.add(e)

    # c.events
    path = 'parliament-test.ics'
    with open(path, 'w') as my_file:
        my_file.writelines(c)

if __name__ == '__main__':
    run()


    # [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
