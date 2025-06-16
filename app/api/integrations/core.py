from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.db.supabase_client import supabase
from app.schemas.integrations import IntegrationsStatusResponse
from app.services.integrations.core import check_google_calendar_integration_status

router = APIRouter()

# Registry of integration status check functions
# Add new integration check functions here as you create them
INTEGRATION_STATUS_CHECKS = {
    "google_calendar": check_google_calendar_integration_status,
    # "microsoft_calendar": check_microsoft_calendar_integration_status, # Example for future
    # "slack": check_slack_integration_status, # Example for future
}

@router.get("/status", response_model=IntegrationsStatusResponse)
async def get_integrations_status(current_user: str = Depends(get_current_user)):
    """
    Checks the connection status of all integrated services for the current user.
    """
    try:
        # Retrieve user's metadata from Supabase
        response = supabase.admin_client.auth.admin.get_user_by_id(current_user)
        user_metadata = response.user.user_metadata

        integration_statuses = {}

        for integration_name, check_func in INTEGRATION_STATUS_CHECKS.items():
            status = await check_func(user_metadata)
            integration_statuses[integration_name] = status

        # Dynamically create the response model instance
        return IntegrationsStatusResponse(**integration_statuses)

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error getting integrations status for user {current_user}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get integrations status: {e}") 