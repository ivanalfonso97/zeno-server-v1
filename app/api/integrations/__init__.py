# This file makes the integrations directory a Python package 

from fastapi import APIRouter
from app.api.integrations.calendar import router as calendar_router
from app.api.integrations.core import router as core_router

router = APIRouter()

# Include the calendar router under /google-calendar
router.include_router(
    calendar_router,
    prefix="/google-calendar",
    tags=["google-calendar"]
)

# Include the core integrations router for general endpoints like /status
router.include_router(
    core_router,
    tags=["integrations"]
) 