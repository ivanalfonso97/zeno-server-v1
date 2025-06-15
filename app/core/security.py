from fastapi import HTTPException, status
from jose import jwt
from app.core.config import settings

def verify_supabase_token(token: str) -> dict:
    """
    Verify a Supabase JWT token and return the payload.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],  # Supabase uses HS256 (HMAC with SHA-256) for JWT signing.
            audience="authenticated"  # Supabase specific audience
        )
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        ) 