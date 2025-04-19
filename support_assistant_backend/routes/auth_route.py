from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from support_assistant_backend.schemas.users import UserCreate, UserRead
from support_assistant_backend.services.auth_service import AuthService
from support_assistant_backend.db.session import get_db

router = APIRouter()

@router.post("/signup", response_model=UserRead)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.signup(user_in)

@router.post("/login")
async def login(form_data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    token = await service.authenticate(form_data.email, form_data.password)
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return token