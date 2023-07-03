from pydantic import BaseModel
import uuid

# create a pydantic model for subjects
class Subject_Create(BaseModel):
    name: str
    user_id: uuid.UUID

# create a pydantic model for subjects responses

class Subject_Response(Subject_Create):
    id: uuid.UUID
    class Config:
        orm_mode = True