from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from support_assistant_backend.models.users import User
from support_assistant_backend.schemas.users import UserCreate
from support_assistant_backend.utils.security import verify_password, get_password_hash, create_access_token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def signup(self, user_in: UserCreate) -> User:
        hashed = get_password_hash(user_in.password)
        user = User(email=user_in.email, hashed_password=hashed)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate(self, email: str, password: str):
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            return None
        access_token = create_access_token({"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}