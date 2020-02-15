
# event data is parsed from JSON

class Event(object):
    
    def __init__(self, startdate, enddate, house, location, description, title, category):
        
        self.mStartDate = startdate
        self.mEndDate = enddate
        self.mHouse = house
        self.mLocation = location
        self.mDescription = description
        self.mTitle = title
        self.mCategory = category


def fakeData():
    
    ObjectArray = [
        Event("2020-03-01T09:30:00", "2020-03-01T11:30:00", "Commons", "Main Chamber", "description 1", "Title 1", "Oral Questions"),
        Event("2020-03-01T11:30:00", "2020-03-01T12:30:00", "Lords", "Westminster Hall", "description 2", "Title 2", "General debate"), 
        Event("2020-03-01T12:30:00", "2020-03-01T14:00:00", "Commons", "Main Chamber", "description 3", "Title 3", "Adjournment")
    ]
    
    return ObjectArray

def transform(event_data):
    # this should return a list or generator of instances of Event()

    return fakeData()