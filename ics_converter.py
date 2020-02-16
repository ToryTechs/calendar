from ics import Calendar, Event, Attendee
from datetime import datetime, timedelta
from functools import reduce

""" End of business in the Main Chamber by days of the week for Commons
    according to https://guidetoprocedure.parliament.uk/articles/5zgbB9yw/moment-of-interruption
    from Monday to Friday (index 0 - 4)
"""
chamber_interruption_hours = [(22, 00), (19, 00), (19, 00), (17, 00), (14, 30), (22,00), (22,00)]


def parse_parliament_event_time(parliament_time):
    """ Convert the time string in the Parliament data to the datetime type in Python
    """
    # datetime.fromisoformat(...) does not work with some Python 3 deployments
    # return datetime.fromisoformat(parliament_time)
    return datetime.strptime(parliament_time, "%Y-%m-%dT%H:%M:%S")


def convert_to_ics_time(time: datetime):
    """ Convert the datetime type in Python into formatted string accepted by the ics library
    """
    return time.isoformat(" ")


def convert_time(time: str):
    """ Streamlined conversion from Parliament time string to formatted time string accepted by the ics library
    """
    return convert_to_ics_time(parse_parliament_event_time(time))


def parse_parliament_groupped_events(groupped_events):
    """ Convert the event entries retrieved from Parliament website into ICS Events
    """
    ics_events_array = []

    for group in groupped_events:

        group_event_array = []
        house = group["House"]
        group_name = group["Name"]

        for event in group["Events"]:
            ics_event = Event()
            if event["DisplayStartTime"] is True:
                ics_event.begin = convert_time(event["StartDateTime"])
            if event["DisplayEndTime"] is True:
                ics_event.end = convert_time(event["EndDateTime"])
            
            ics_event.name = event["Title"]
            ics_event.description = event["Description"]
            if event["Location"] is not None:
                ics_event.location = event["Location"]
            else:
                ics_event.location = group_name
            # Multiple categories are created for easier event management in the clients' calendar software
            ics_event.categories = [event["Category"], house, group_name]

            for member in event["Members"]:
                # MP's real email address is supposed to be used.  Here, the placeholder format is name@house.
                # Mapping to real email address to be implemented in the future.
                attendee = Attendee("%s@%s" % (member["Name"].replace(" ", ""), house), member["Name"])
                ics_event.attendees.add(attendee)

            group_event_array.append(ics_event)

        
        if len(group_event_array) <= 0:
            continue

        try:
        #if True:
            """
                The following segemnts of code deal with the problem that the some event entries scraped from 
                the Parliament website do not have a start time, an end time or both.

                For Main Chamber sessions, sessions end times may be flexible.  So, the solution is to set
                the Adjournment session to begin at the interruption of the day.  The durations of sessions
                between the session with a last known start time and the Adjournment session are equally divided.

                For non-Main Chamber sessions, the duration of the last event of the day (if the end time is not available)
                is set to be the same as the preceding session.
            """

            for index in range(0, len(group_event_array)):
                # Use the start time of the next event as the end time for a event.
                index_next = index + 1
                index_previous = index - 1
                if index < len(group_event_array) - 1:
                    if group["Events"][index]["DisplayEndTime"] is False and group["Events"][index_next]["DisplayStartTime"] is True:
                        group_event_array[index].end = group_event_array[index_next].begin

                elif index > 0 and index == len(group_event_array) - 1:
                    # the last event is handled differently for Main Chamber and Grand Committee events
                    # so they are excluded
                    if group_name not in ["Main Chamber", "Grand Committees"] and group["Events"][index]["DisplayEndTime"] is False:
                        duration_of_previous_session = parse_parliament_event_time(group["Events"][index]["StartDateTime"]) - parse_parliament_event_time(group["Events"][index_previous]["StartDateTime"])
                        group_event_array[index].end = convert_to_ics_time(parse_parliament_event_time(group["Events"][index]["StartDateTime"]) + duration_of_previous_session)
            

            if group_name in ["Main Chamber", "Grand Committees"]:
                # The special treatment for Main Chamber and Grand Committee events
                # First, get the last event with a known start time
                # If a start time is assigned to the last session, the start time of that last session not counted.
                main_chamber_event_start_times = list([e["StartDateTime"] for e in group["Events"][:-1] if e["DisplayStartTime"] is True]) if group["Events"][-1]["DisplayStartTime"] is True and len(group["Events"]) > 1 else list([e["StartDateTime"] for e in group["Events"] if e["DisplayStartTime"] is True])
                if len(main_chamber_event_start_times) > 0:
                    latest_start_time_str = reduce(lambda x, y: x if x > y else y, main_chamber_event_start_times)
                    last_event_index = len(group_event_array) - 1
                    latest_start_time = parse_parliament_event_time(latest_start_time_str)
                    # Then, calculate the interruption time of the day
                    day_of_week_index = latest_start_time.weekday()
                    last_event_start_time = datetime(latest_start_time.year, latest_start_time.month, latest_start_time.day,
                                                       chamber_interruption_hours[day_of_week_index][0],
                                                       chamber_interruption_hours[day_of_week_index][1])
                    if house == "Lords":
                        last_event_start_time = datetime(latest_start_time.year, latest_start_time.month, latest_start_time.day, 22, 30)

                    last_event_is_adjournment = True if group_event_array[last_event_index].name in ["Adjournment", "Estimated rising time"] else False

                    if last_event_is_adjournment is True:
                        if house == "Lords" and group["Events"][last_event_index]["DisplayStartTime"] is True:
                            group_event_array[last_event_index].end = group_event_array[last_event_index].begin
                            last_event_start_time = parse_parliament_event_time(group["Events"][last_event_index]["StartDateTime"])
                        else:
                            # Set the start time and end time for the last session which is an adjournment session
                            group_event_array[last_event_index].begin = convert_to_ics_time(last_event_start_time)
                            group_event_array[last_event_index].end = convert_to_ics_time(last_event_start_time + timedelta(minutes=30))
                        group_event_array[last_event_index - 1].end = group_event_array[last_event_index].begin
                    else:
                        # Set the end time for the last session which is not an adjournment session
                        group_event_array[last_event_index].end = convert_to_ics_time(last_event_start_time)

                    # Figure out the index of the last session without unknown start time
                    # If a start time is assigned to the last session, that last session not counted.
                    event_with_latest_start_time_index = 0
                    for index in range(last_event_index - 1, -1, -1): 
                        if group["Events"][index]["DisplayStartTime"] is True and index != (len(group["Events"]) - 1):
                            event_with_latest_start_time_index = index
                            break

                    # Equally divide the time between the session with last known start time and the adjournment session (or the end time of the last session, if not an adjournment session)
                    if last_event_index > event_with_latest_start_time_index: 
                        if last_event_is_adjournment is True:
                            event_duration = (last_event_start_time - latest_start_time) / (last_event_index - event_with_latest_start_time_index)
                        else:
                            event_duration = (last_event_start_time - latest_start_time) / (last_event_index - event_with_latest_start_time_index + 1)
                    else:
                        event_duration = last_event_start_time - latest_start_time
                    seq = 1
                    for index in range(event_with_latest_start_time_index + 1, last_event_index if last_event_is_adjournment is True else last_event_index + 1):
                        group_event_array[index].begin = convert_to_ics_time(latest_start_time + (event_duration * seq))
                        if group_event_array[index - 1].begin <= group_event_array[index].begin:
                            group_event_array[index - 1].end = group_event_array[index].begin
                            seq = seq + 1
        except:
            # Raw data might be dirty.  Dirty data may casue the time spacing calaculating to fail.
            # In any case, an exception should not prevented an event from being added to the calendar.
            # Event entries with dirty start time and end time will be dealt with in the following segment of code.
            print("Exception caught while calculating event duration")


        for index in range(0, len(group_event_array)):
            # some events do not have any start time assigned to them yet
            # in this case, just use the 00 hours time of the date as in the raw data
            if group_event_array[index].begin is None:
                group_event_array[index].begin = convert_time(group["Events"][index]["StartDateTime"])
            if group_event_array[index].end is None:
                group_event_array[index].end = convert_time(group["Events"][index]["EndDateTime"])
            
            # generate an uid for every event record
            # see RFC 2445 (page 110) and RFC 822 for the suggested uid format 
            # our uid is based on the start time, it has to be done at the very end
            group_event_array[index].uid = "%s-%d@%s.%s" % (group_event_array[index].begin.strftime("%Y%m%dT%H%M%S"), index, group_name.replace(" ", ""), house.replace(" ", "")) 

        # merge the groupped events into a single array
        ics_events_array.extend(group_event_array)

    return ics_events_array


def add_ics_events_to_calendar(ics_event_array):
    """ create a calendar and then add the events to the calendar
    """
    calendar = Calendar()
    calendar.creator = "ToryTechs#1 Hackathon Calendar Team"
    for event in ics_event_array:
        calendar.events.add(event)
    return calendar
