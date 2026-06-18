from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashes a plaintext password for safe database storage.
def hash_password(password: str) -> str:
    return password_context.hash(password)

# Verifies a plaintext password against a stored password hash.
def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

# Creates a signed JWT access token with an expiry timestamp.
def create_access_token(subject: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    payload = {"sub": subject, "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

# Decodes a JWT and returns the subject if the token is valid.
def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload.get("sub")
    except JWTError:
        return None
