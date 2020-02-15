
# event data is parsed from JSON

class Event(object):
    
    def __init__(self, startdate, enddate, house, location, description, title, category, members, displayStartDate, displayEndDate):
        
        self.mStartDate = startdate
        self.mEndDate = enddate
        self.mHouse = house
        self.mLocation = location
        self.mDescription = description
        self.mTitle = title
        self.mCategory = category
        self.mMembers = members
        self.mDisplayStartDate = displayStartDate
        self.mDisplayEndDate = displayEndDate


def fakeData():
    
    ObjectArray = [
        Event("2020-03-01T09:30:00", "2020-03-01T11:30:00", "Commons", "Main Chamber", "description 1", "Title 1", "Oral Questions", [{
            "Name": "Baroness Gale",
            "BiographyUrl": "http://www.parliament.uk/biographies/lords/baroness-gale/2503" 
        }], "true", "true"),
        Event("2020-03-01T11:30:00", "2020-03-01T12:30:00", "Lords", "Westminster Hall", "description 2", "Title 2", "General debate", [{
            "Name": "",
            "BiographyUrl": ""
        }], "false", "true"), 
        Event("2020-03-01T12:30:00", "2020-03-01T14:00:00", "Commons", "Main Chamber", "description 3", "Title 3", "Adjournment", [{
            "Name": "",
            "BiographyUrl": ""     
        }], "true", "true")
    ]
    
    return ObjectArray

def transform(event_data):
    # this should return a list or generator of instances of Event()
    results = event_data["Results"]["Groupings"]
    
    eventArray = []
    for key in results:
        events = key["Events"]
        for event in events:
            startdate = event["StartDateTime"]
            enddate = event["EndDateTime"]
            house = event["House"]
            location = event["EventType"]
            description = event["Description"]
            title = event["Title"]
            category = event["Category"]
            members = event["Members"]
            displaystart = event["DisplayStartTime"]
            displayend = event["DisplayEndTime"]
            eventArray.append(Event(startdate, enddate, house, location, description, title, category, members, displaystart, displayend))
            
    return eventArray