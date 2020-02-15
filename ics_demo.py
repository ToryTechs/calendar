from ics import Calendar, Event, Organizer, Attendee


c = Calendar()
e = Event()
e.name = "Tory meetup"
e.begin = '2014-01-01 00:00:00'

organiser1 = Organizer("mpemail@theserver.com", "The Organiser")
e.organizer = organiser1

attendee1 = Attendee("reesmogg@theserver.com", "Macob Rees-Mogg")
attendee2 = Attendee("borisjohnson@theserver.com", "Boris Johnson")

e.attendees.add(attendee1)
e.attendees.add(attendee2)

c.events.add(e)
c.events

with open('my.ics', 'w') as my_file:
    my_file.writelines(c)
