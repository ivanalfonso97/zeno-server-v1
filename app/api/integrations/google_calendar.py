import jwt
from datetime import datetime
from google_auth_oauthlib.flow import Flow
from fastapi.responses import RedirectResponse
from google.oauth2.credentials import Credentials
from fastapi import APIRouter, HTTPException, Depends, Request

from app.core.config import settings
from app.api.deps import get_current_user
from app.db.supabase_client import supabase
from app.schemas.integrations.google_calendar import GoogleCalendarAuthUrlResponse
from app.services.integrations.google_calendar import get_google_calendar_events, get_google_flow, get_google_credentials

router = APIRouter()

@router.get("/auth-url", response_model=GoogleCalendarAuthUrlResponse)
async def get_google_calendar_auth_url(current_user: str = Depends(get_current_user)):
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
        
        linked_google_email = None
        if credentials.id_token:
            # Decode the ID token to get user info (email)
            # The ID token is a JWT, its payload contains user claims
            try:
                id_token_info = jwt.decode(
                    credentials.id_token, options={"verify_signature": False}
                )
                linked_google_email = id_token_info.get("email")
            except Exception as e:
                print(f"Error decoding ID token: {e}")
                # Log error but don't fail the entire process

        # Update user's metadata in Supabase using the admin client
        updated_metadata = {
            "google_access_token": credentials.token,
            "google_token_expiry": credentials.expiry.isoformat(),
            "google_refresh_token": credentials.refresh_token,
        }
        if linked_google_email:
            updated_metadata["google_calendar_linked_email"] = linked_google_email

        try:
            supabase.admin_client.auth.admin.update_user_by_id(
                user_id,
                {
                    "user_metadata": updated_metadata
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

@router.get("/events")
async def get_calendar_events(current_user: str = Depends(get_current_user)):
    """
    Fetches Google Calendar events for the authenticated user.
    """
    try:
        # Retrieve user's Google Calendar tokens from Supabase metadata
        credentials = await get_google_credentials(current_user)

        # Use the credentials to fetch events
        events = await get_google_calendar_events(credentials)
        return {"events": events}

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error fetching events for user {current_user}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch Google Calendar events: {e}") 