from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from app.models.calendar import GoogleCalendarAuthUrlResponse
from app.core.config import settings
from app.api.deps import get_current_user
from google_auth_oauthlib.flow import Flow
from app.db.supabase_client import supabase

router = APIRouter()

# Google Calendar API scope - read-only access
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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

@router.get("/auth-url", response_model=GoogleCalendarAuthUrlResponse)
async def get_google_calendar_auth_url(current_user: str = Depends(get_current_user)):
    print("DEBUG: Endpoint hit - /auth-url")
    print("DEBUG: User ID:", current_user)
    print("DEBUG: Settings:", {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_CALENDAR_REDIRECT_URI
    })
    try:
        # Create OAuth2 flow
        flow = get_google_flow()

        # Generate authorization URL
        auth_url, _ = flow.authorization_url(
            access_type='offline',  # Get refresh token
            include_granted_scopes='true',
            prompt='consent',  # Force consent screen to get refresh token
            state=current_user
        )

        return GoogleCalendarAuthUrlResponse(auth_url=auth_url)
    except Exception as e:
        print("Error generating auth URL:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to generate Google Calendar auth URL"
        )

@router.get("/callback")
async def google_calendar_callback(
    request: Request,
    # current_user: str = Depends(get_current_user)
    state: str = None
):
    """
    Handle the OAuth callback from Google Calendar.
    Redirects back to the frontend with tokens or error status.
    """
    try:
        # Get the authorization code from the query parameters
        code = request.query_params.get("code")
        if not code:
            return RedirectResponse(
                url=f"{settings.FRONTEND_URL}/integrations/link-google-calendar?error=no_code"
            )
        
        # Get the user ID from the state parameter
        user_id = state
        if not user_id:
            return RedirectResponse(
                url=f"{settings.FRONTEND_URL}/integrations/link-google-calendar?error=no_user_id_in_state"
            )

        # Create OAuth2 flow
        flow = get_google_flow()

        # Exchange the authorization code for tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials

        # Update user's metadata in Supabase using the admin client
        try:
            supabase.admin_client.auth.admin.update_user_by_id(
                user_id,
                {
                    "user_metadata": {
                        "google_access_token": credentials.token,
                        "google_token_expiry": credentials.expiry.isoformat(),
                        "google_refresh_token": credentials.refresh_token
                    }
                }
            )
        except Exception as e:
            print("Error updating user metadata:", str(e))
            raise HTTPException(
                status_code=500,
                detail="Failed to update user metadata with Google Calendar tokens"
            )

        # Redirect back to frontend with success
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/integrations/link-google-calendar?status=success"
        )

    except Exception as e:
        print("Error in callback:", str(e))
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/integrations/link-google-calendar?status=error&message={str(e)}"
        ) 