# This file makes the integrations directory a Python package 

from fastapi import APIRouter
from app.api.integrations.calendar import router as calendar_router

router = APIRouter()

# Include the calendar router under /google-calendar
router.include_router(
    calendar_router,
    prefix="/google-calendar",
    tags=["google-calendar"]
) 