from app.db.supabase_client import supabase
from fastapi import APIRouter, HTTPException
from app.models.auth import LoginRequest, LoginResponse, UserResponse

router = APIRouter()

@router.get("/")
async def auth_root():
    return {"message": "Auth endpoints"}

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        response = await supabase.login(request.email, request.password)
        return LoginResponse(
            access_token=response.session.access_token,
            user=UserResponse(
                id=response.user.id,
                email=response.user.email
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
