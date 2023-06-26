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

class All_Students(Student_Create):
    id: uuid.UUID
    class Config:
        orm_mode = True
    
# create a pydantic model for students response
class Student_Response(All_Students):
    level_name: str
    institution_name: str
    user_id: uuid.UUID
    person_id: uuid.UUID
    created_by: str
