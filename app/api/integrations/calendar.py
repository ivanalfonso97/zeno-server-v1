from fastapi import APIRouter, HTTPException, Depends
from app.models.calendar import GoogleCalendarAuthUrlResponse
from app.core.config import settings
from app.api.deps import get_current_user
from google_auth_oauthlib.flow import Flow

router = APIRouter()

# Google Calendar API scope - read-only access
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

@router.get("/auth-url", response_model=GoogleCalendarAuthUrlResponse)
async def get_google_calendar_auth_url(current_user: str = Depends(get_current_user)):
    print("DEBUG: Endpoint hit - /auth-url")
    print("DEBUG: User ID:", current_user)
    print("DEBUG: Settings:", {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI
    })
    try:
        # Create OAuth2 flow
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )

        # Generate authorization URL
        auth_url, _ = flow.authorization_url(
            access_type='offline',  # Get refresh token
            include_granted_scopes='true',
            prompt='consent'  # Force consent screen to get refresh token
        )

        return GoogleCalendarAuthUrlResponse(auth_url=auth_url)
    except Exception as e:
        print("Error generating auth URL:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to generate Google Calendar auth URL"
        ) 