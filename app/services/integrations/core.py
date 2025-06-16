from typing import Dict, Any
from datetime import datetime, timezone

from app.schemas.integrations import IntegrationStatus

async def check_google_calendar_integration_status(user_metadata: Dict[str, Any]) -> IntegrationStatus:
    """
    Checks the status of the Google Calendar integration based on user metadata.
    Args:
        user_metadata: The user's metadata dictionary from Supabase.
    Returns:
        An IntegrationStatus object for Google Calendar.
    """
    google_refresh_token = user_metadata.get("google_refresh_token")
    linked_google_calendar_email = user_metadata.get("google_calendar_linked_email")

    is_connected = False
    error_message = None

    if google_refresh_token:
        is_connected = True
    else:
        error_message = "Missing Google Calendar refresh token. Please re-link your account."

    return IntegrationStatus(
        is_connected=is_connected,
        last_checked_at=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        error_message=error_message,
        linked_google_calendar_email=linked_google_calendar_email
    ) 