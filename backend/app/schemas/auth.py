from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    portfolio_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    linkedin_url: HttpUrl | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    portfolio_url: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None

    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    request_id: str
    access_token: str
    token_type: str = "bearer"
    user: UserRead

class MeResponse(BaseModel):
    request_id: str
    user: UserRead
