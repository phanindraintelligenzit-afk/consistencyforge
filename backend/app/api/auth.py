"""Auth API router — register, login, me endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Simple in-memory user store (replace with DB in production)
_users_db: dict[str, dict] = {}


def _get_fake_user_table():
    return _users_db


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest):
    """Register a new user."""
    users = _get_fake_user_table()
    if req.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    if any(u.get("email") == req.email for u in users.values()):
        raise HTTPException(status_code=400, detail="Email already exists")

    user = {
        "id": str(len(users) + 1),
        "username": req.username,
        "email": req.email,
        "hashed_password": hash_password(req.password),
        "is_active": True,
    }
    users[req.username] = user
    return UserResponse(id=user["id"], username=user["username"], email=user["email"], is_active=True)


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    """Authenticate and return a JWT token."""
    users = _get_fake_user_table()
    user = users.get(req.username)
    if not user or not verify_password(req.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user["username"], "id": user["id"]})
    return TokenResponse(access_token=token, expires_in=3600)


@router.get("/me", response_model=UserResponse)
async def get_current_user(authorization: Optional[str] = None):
    """Return the current authenticated user's info."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    users = _get_fake_user_table()
    user = users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(id=user["id"], username=user["username"], email=user["email"], is_active=user["is_active"])