from app.db.supabase_client import supabase
from fastapi import APIRouter, HTTPException
from app.models.auth import SignupRequest, LoginRequest, UserResponse, SignupResponse, LoginResponse 

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
    except HTTPException as e:
        # Re-raise HTTP exceptions from client
        raise e
    except Exception:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during login"
        )

@router.post("/signup", response_model=SignupResponse)
async def signup(request: SignupRequest):
    try:
        response = await supabase.signup(
            request.email, 
            request.password, 
            request.first_name, 
            request.last_name
        )
        return SignupResponse(
            access_token=response.session.access_token,
            user=UserResponse(
                id=response.user.id,
                email=response.user.email
            )
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during signup"
        )