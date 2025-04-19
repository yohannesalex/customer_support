# Import necessary modules for handling authentication, exceptions, and database interaction.
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select # Added import for select
from support_assistant_backend.db.session import get_db
from support_assistant_backend.models.users import User
from support_assistant_backend.utils.security import verify_password
from support_assistant_backend.core.config import settings

# tokenUrl specifies the endpoint where clients can obtain a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Define an asynchronous dependency function to get the current authenticated user.
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    # Define the exception to be raised if credentials cannot be validated.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token using the secret key and algorithm from settings.
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Query the database asynchronously to find the user by their ID.
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none() 

    # If the user is not found in the database, raise a credentials exception.
    if user is None:
        raise credentials_exception

    return user