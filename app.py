import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set in .env"
    )

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

app = FastAPI(
    title="FlyRank Auth API",
    description="Supabase authentication and protected API",
    version="1.0.0"
)


class AuthRequest(BaseModel):
    email: str
    password: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Server running and connected to Supabase"
    }


@app.post("/auth/signup")
def signup(data: AuthRequest):
    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })

        if response.user is None:
            raise HTTPException(
                status_code=400,
                detail="Signup failed"
            )

        return {
            "message": "Signup successful",
            "user_id": response.user.id,
            "email": response.user.email
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/auth/login")
def login(data: AuthRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        if response.user is None or response.session is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user_id": response.user.id,
            "email": response.user.email
        }
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )