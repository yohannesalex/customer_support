from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from support_assistant_backend.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify if the plain password matches the hashed password.
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Hash the provided password using bcrypt.
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Encode the payload into a JWT.
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt