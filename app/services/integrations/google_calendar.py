from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

async def get_google_calendar_events(credentials: Credentials):
    """
    Fetches events from the user's Google Calendar.
    Args:
        credentials: Google OAuth2 credentials object.
    Returns:
        A list of calendar events.
    """
    try:
        service = build('calendar', 'v3', credentials=credentials)

        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events

    except Exception as e:
        print(f"Error fetching Google Calendar events: {e}")
        # In a real application, you might want to re-raise a specific exception
        # or return an error status.
        return [] 