from ics import Calendar, Event, Organizer, Attendee
from datetime import datetime, timedelta
from functools import reduce

""" End of business in the Main Chamber by days of the week
    according to https://guidetoprocedure.parliament.uk/articles/5zgbB9yw/moment-of-interruption
    from Monday to Friday (index 0 - 4)
"""
chamber_interruption_hours = [(22, 00), (19, 00), (19, 00), (17, 00), (14, 30)]


def parse_parliament_event_time(parliament_time):
    """ Convert the time string in the Parliament data to the datetime type in Python
    """
    return datetime.fromisoformat(parliament_time)


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
                # the last event is handled differently for Main Chamber events
                # so they are excluded
                if group_name != "Main Chamber":
                    if group["Events"][index]["DisplayEndTime"] is False:
                        duration_of_previous_session = parse_parliament_event_time(group["Events"][index]["StartDateTime"]) - parse_parliament_event_time(group["Events"][index_previous]["StartDateTime"])
                        group_event_array[index].end = convert_to_ics_time(parse_parliament_event_time(group["Events"][index]["StartDateTime"]) + duration_of_previous_session)
            

        if group_name == "Main Chamber":
            # The special treatment for Main Chamber events
            # First, get the last event with a known start time
            main_chamber_event_start_times = [e["StartDateTime"] for e in group["Events"] if e["DisplayStartTime"] is True]
            latest_start_time_str = reduce(lambda x, y: x if x > y else y, main_chamber_event_start_times)
            last_event_index = len(group_event_array) - 1
            latest_start_time = parse_parliament_event_time(latest_start_time_str)
            # Then, calculate the interruption time of the day
            day_of_week_index = latest_start_time.weekday()
            last_event_start_time = datetime(latest_start_time.year, latest_start_time.month, latest_start_time.day,
                                                chamber_interruption_hours[day_of_week_index][0],
                                                chamber_interruption_hours[day_of_week_index][1])
            # Set the start time and end time for the adjournment session
            group_event_array[last_event_index].begin = convert_to_ics_time(last_event_start_time)
            group_event_array[last_event_index].end = convert_to_ics_time(last_event_start_time + timedelta(minutes=30))
            group_event_array[last_event_index - 1].end = group_event_array[last_event_index].begin

            # Figure out the index of the last session without unknown start time
            event_with_latest_start_time_index = 0
            for index in range(last_event_index - 1, -1, -1):
                if group["Events"][index]["DisplayStartTime"] is True:
                    event_with_latest_start_time_index = index
                    break

            # Equally divide the time between the session with last known start time and the adjournment session 
            event_duration = (last_event_start_time - latest_start_time) / (last_event_index - event_with_latest_start_time_index)

            seq = 1
            for index in range(event_with_latest_start_time_index + 1, last_event_index):
                group_event_array[index].begin = convert_to_ics_time(latest_start_time + (event_duration * seq))
                group_event_array[index - 1].end = group_event_array[index].begin
                seq = seq + 1


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
    calendar.creator = "ToryTech#1 Calendar Team"
    for event in ics_event_array:
        calendar.events.add(event)
    return calendar
