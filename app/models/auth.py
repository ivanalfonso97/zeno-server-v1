from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    id: str

class LoginResponse(BaseModel):
    access_token: str
    user: UserResponse

class SignupResponse(BaseModel):
    access_token: str
    user: UserResponse