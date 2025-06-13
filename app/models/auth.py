from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str

class LoginResponse(BaseModel):
    access_token: str
    user: UserResponse