from pydantic import BaseModel
from datetime import datetime

class GoogleCalendarAuthUrlResponse(BaseModel):
    auth_url: str
 
class GoogleCalendarTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: datetime 