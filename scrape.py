#!/usr/bin/env python3

import requests

def get_all_calendar_data():
    url = "https://calendar.parliament.uk/Calendar/Refresh"

    params = {
        "StartDate": "2020-02-06T00:00:00.000Z",
        "ViewBy": "Daily",
        "House": "Commons",
        "EventGrouping": "All"
    }

    req = requests.post(url, data=params)
    return req.json()

def run():
    print(get_all_calendar_data())

if __name__ == '__main__':
    run()
