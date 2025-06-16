from pydantic import BaseModel, Field
from typing import Optional

class IntegrationStatus(BaseModel):
    is_connected: bool = Field(..., description="True if the integration is connected and tokens are present.")
    last_checked_at: Optional[str] = Field(None, description="Timestamp of when the integration status was last checked.")
    error_message: Optional[str] = Field(None, description="An error message if the connection is problematic.")

class IntegrationsStatusResponse(BaseModel):
    google_calendar: IntegrationStatus = Field(..., description="Status of the Google Calendar integration.")
    # Add more integrations here as needed, e.g.,
    # microsoft_calendar: IntegrationStatus = Field(..., description="Status of the Microsoft Calendar integration.")
    # slack: IntegrationStatus = Field(..., description="Status of the Slack integration.")