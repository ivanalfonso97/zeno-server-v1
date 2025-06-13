from supabase import create_client, Client
from fastapi import HTTPException
from app.core.config import settings

# Python Supabase documentation: https://supabase.com/docs/reference/python/introduction

class SupabaseClient:
    def __init__(self):
        print("Supabase URL:", settings.SUPABASE_URL)
        print("Supabase Key:", settings.SUPABASE_KEY)
        
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )

    async def login(self, email: str, password: str):
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return response
        except Exception as e:
            error_message = str(e)
            if "Invalid login credentials" in error_message:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid email or password"
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="An error occurred during login"
                )
    
    async def signup(self, email: str, password: str, first_name: str, last_name: str):
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                    }
                }
            })
            return response
        except Exception as e:
            error_message = str(e)
            print("IC01",error_message)
            if "User already registered" in error_message:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )
            elif "Password" in error_message:
                raise HTTPException(
                    status_code=400,
                    detail="Password does not meet requirements"
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="An error occurred during signup"
                )

# Create a singleton instance
supabase = SupabaseClient() 