#!/usr/bin/env python3

import requests
import json
from datetime import datetime

#def get_all_calendar_data():
#    url = "https://calendar.parliament.uk/Calendar/Refresh"
#
#    params = {
#        "StartDate": "2020-02-06T00:00:00.000Z",
#        "ViewBy": "Daily",
#        "House": "Commons",
#        "EventGrouping": "All"
#    }

#    req = requests.post(url, data=params)
#    return req.json()


def get_parliament_events_data(date: datetime, house: str):
    url = "https://calendar.parliament.uk/Calendar/Refresh"
    
    params = {
        "StartDate": date.isoformat(),
        "ViewBy": "Daily",
        "House": house,
        "EventGrouping": "All"
    }

    req = requests.post(url, data=params)
    return req.json()


#def test_run():
    # print(get_all_calendar_data())
#    print(get_events(datetime.strptime("2020-02-19", "%Y-%m-%d"), "Commons"))
    

#if __name__ == '__main__':
#    test_run()
