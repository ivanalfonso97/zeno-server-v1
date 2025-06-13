from supabase import create_client, Client
from fastapi import HTTPException
from app.core.config import settings

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
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

# Create a singleton instance
supabase = SupabaseClient() 