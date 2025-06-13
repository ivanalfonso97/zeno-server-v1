from fastapi import APIRouter
from .auth import router as auth_router
# from .chat import router as chat_router
# from .integrations import router as integrations_router
# from .tasks import router as tasks_router
# from .companies import router as companies_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
# api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
# api_router.include_router(integrations_router, prefix="/integrations", tags=["Integrations"])
# api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
# api_router.include_router(companies_router, prefix="/companies", tags=["Companies"])
