import datetime
from .calendar_auth import authenticate_calendar

def create_calendar_event(
        summary: str, 
        start_time: str,
        end_time: str,
        timezone: str,
        location: str,
        description: str,
        attendees: list,
):
    """
    This function creates a calendar event. 
    Args:
        summary (str): The title of the event.
        start_time (str): The start time of the event in ISO format (e.g., '2023-10-01T10:00:00Z').
        end_time (str): The end time of the event in ISO format (e.g., '2023-10-01T11:00:00Z').
        timezone (str): The timezone of the event (e.g., 'Asia/Kolkata').
        location (str): The location of the event (optional).
        description (str): A description of the event (optional).
        attendees (list): A list of email addresses for the event attendees (optional).
    Returns:
        a dict with the 'status' of the event creation or the error details.
    """
    
    service = authenticate_calendar()
    if service is None:
        return {
            "status": "error",
            "message": "Failed to authenticate with Google Calendar API."
        }
    if start_time or end_time is None:
        return {
            "status": "error",
            "message": "Start time and end time are required."
        }
    
    if timezone is None:
        timezone = 'Asia/Kolkata'
    else:
        timezone = timezone.strip()

    event_request = {
        'summary': summary,
        'start': {
            'dateTime': datetime.strptime(start_time),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': datetime.strptime(end_time),
            'timeZone': timezone,
        },
    }
    
    if location:
        event['location'] = location
    
    if description:
        event['description'] = description
    
    if attendees:
        event['attendees'] = [{'email': attendee} for attendee in attendees]    
    
    event = service.events().insert(calendarId='primary', body=event_request).execute()

    return {
        "status": "success",
        "message": "Event created successfully.",
        "event_id": event['id'],
        "event_link": event.get("htmlLink", ""),
    }