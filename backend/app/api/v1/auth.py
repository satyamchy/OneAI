from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import MeResponse, TokenResponse, UserCreate, UserLogin
from app.utils.request_id import generate_request_id

router = APIRouter(prefix="/auth", tags=["auth"])

# Registers a new user and returns a JWT access token.
@router.post("/register", response_model=TokenResponse)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    request_id = generate_request_id()
    existing = await db.execute(select(User).where(User.email == payload.email.lower()))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(
        email=payload.email.lower(),
        hashed_password=hash_password(payload.password),
        portfolio_url=str(payload.portfolio_url) if payload.portfolio_url else None,
        github_url=str(payload.github_url) if payload.github_url else None,
        linkedin_url=str(payload.linkedin_url) if payload.linkedin_url else None,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return TokenResponse(request_id=request_id, access_token=create_access_token(str(user.id)), user=user)

# Authenticates an existing user and returns a JWT access token.
@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    request_id = generate_request_id()
    result = await db.execute(select(User).where(User.email == payload.email.lower()))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(request_id=request_id, access_token=create_access_token(str(user.id)), user=user)

# Returns the currently authenticated user.
@router.get("/me", response_model=MeResponse)
async def me(user: User = Depends(get_current_user)):
    return MeResponse(request_id=generate_request_id(), user=user)
