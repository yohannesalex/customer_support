from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from support_assistant_backend.models.users import User
from support_assistant_backend.schemas.users import UserCreate
from support_assistant_backend.utils.security import verify_password, get_password_hash, create_access_token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def signup(self, user_in: UserCreate) -> User:
        # Hash the user's password before storing.
        hashed = get_password_hash(user_in.password)
        user = User(email=user_in.email, hashed_password=hashed, role=user_in.role)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate(self, email: str, password: str):
        # Retrieve user by email from the database.
        user = await self.get_user_by_email(email)
        # Verify password and generate access token if successful.
        if not user or not verify_password(password, user.hashed_password):
            return None
        access_token = create_access_token({"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
