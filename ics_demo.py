from ics import Calendar, Event, Organizer, Attendee


c = Calendar()
e = Event()
e.name = "Oral questions"

# If DisplayStartTime is false, do not use the start time
# If DisplayEndTime is false, do not use the end time

# For Main Chamber events without an end time epsecified, the end time should be:
# Mon 22:00
# Tue 19:00
# Wed 19:00
# Thurs 17:00
# Fri 14:30
# For Adjournment, the time for the day specified above + 30 mins

e.begin = "2020-02-26 15:00:00"
e.end = "2020-02-26 19:00:00"

e.uid = "12334"
e.description = "Government's response to the report ' A perverse and ominous enterprise: the death penalty and illegal executions in Saudi Arabia'"
e.location = "Lords"
e.categories = ["Oral questions"]

organiser1 = Organizer("mpemail@theserver.com", "The Organiser")
e.organizer = organiser1

attendee1 = Attendee("Whitaker@theserver.com", "Baroness Whitaker")
e.attendees.add(attendee1)

c.events.add(e)
c.events

with open('my.ics', 'w') as my_file:
    my_file.writelines(c)
