from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

# create a pydantic model for user
class User_Base(BaseModel):
    firstname: str
    lastname: str
    institution_id: uuid.UUID

class User_Create(User_Base):
    password: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

# create a pydantic model for user response
class User_Login(User_Base):
    id: uuid.UUID
    is_superuser: bool
    is_admin: bool
    is_teacher: bool
    class Config:
        orm_mode = True

class User_Response(User_Login):
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

# create a pydantic model for update user
class User_Update(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    institution_id: uuid.UUID = None
    password: Optional[str] = None