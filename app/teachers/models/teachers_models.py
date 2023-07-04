from pydantic import BaseModel
import uuid

# create a class for the model
class Teachers_Create(BaseModel):
    student_id: uuid.UUID
    teacher_id: uuid.UUID

class Teachers_Response(Teachers_Create):
    id: uuid.UUID
    teacher: str
    class Config:
        orm_mode = True