from pydantic import BaseModel

class GoogleCalendarAuthUrlResponse(BaseModel):
    auth_url: str 