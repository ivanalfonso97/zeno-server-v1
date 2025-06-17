from datetime import datetime
from fastapi import HTTPException
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from app.core.config import settings
from app.db.supabase_client import supabase

# Google Calendar API scope
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

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

def get_google_flow() -> Flow:
    """Get configured Google OAuth flow."""
    return Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_CALENDAR_REDIRECT_URI
    )

async def get_google_credentials(user_id: str) -> Credentials:
    """
    Retrieves Google Calendar credentials from Supabase user metadata.
    Args:
        user_id: The ID of the user whose credentials to retrieve.
    Returns:
        A Google Credentials object.
    Raises:
        HTTPException: If Google Calendar integration is not found for the user.
    """
    response = supabase.admin_client.auth.admin.get_user_by_id(user_id)
    user_metadata = response.user.user_metadata

    google_access_token = user_metadata.get("google_access_token")
    google_token_expiry = user_metadata.get("google_token_expiry")
    google_refresh_token = user_metadata.get("google_refresh_token")

    if not all([google_access_token, google_token_expiry, google_refresh_token]):
        raise HTTPException(
            status_code=404,
            detail="Google Calendar integration not found for this user. Please link your account."
        )

    # Create Google Credentials object
    credentials = Credentials(
        token=google_access_token,
        refresh_token=google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=SCOPES,
        expiry=datetime.fromisoformat(google_token_expiry.replace('Z', '+00:00')) if google_token_expiry else None
    )
    return credentials 