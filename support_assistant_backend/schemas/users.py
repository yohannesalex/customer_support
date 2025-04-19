# define schemas for user creation and reading
from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role : str = "user"  # Default role is 'user'
  
class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    role: str

    class Config:
        orm_mode = True