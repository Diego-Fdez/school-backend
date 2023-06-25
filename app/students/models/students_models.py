from pydantic import BaseModel
from typing import Optional
import uuid

# create a pydantic model for students
class Student_Create(BaseModel):
    identification: str
    contact: Optional[str] = None
    level_id: uuid.UUID
    observations: Optional[str] = None
    firstname: str
    lastname: str
    address: Optional[str] = None
    phone: Optional[str] = None
    institution_id: uuid.UUID
    
# create a pydantic model for students response
class Student_Response(Student_Create):
    id: uuid.UUID
    level_name: str
    institution_name: str
    user_id: uuid.UUID
    person_id: uuid.UUID
    class Config:
        orm_mode = True

class Student_Update(BaseModel):
    identification: Optional[str] = None
    contact: Optional[str] = None
    level_id: Optional[uuid.UUID] = None
    observations: Optional[str] = None
    user_id: Optional[uuid.UUID] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    institution_id: Optional[uuid.UUID] = None