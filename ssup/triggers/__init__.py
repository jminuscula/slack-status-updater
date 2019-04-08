
from ssup.triggers.googlecalendar import GoogleCalendarEventTrigger
from ssup.triggers.process import ProcessEventTrigger


googlecalendar = GoogleCalendarEventTrigger
process = ProcessEventTrigger


__all__ = [
    'googlecalendar',
    'process',
]
