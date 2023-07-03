from pydantic import BaseModel
import uuid

# create a pydantic model for rooms class
class RoomBase(BaseModel):
    name: str

# create a pydantic model for all rooms class
class All_Rooms(BaseModel):
    id: uuid.UUID
    name: str
    class Config:
        orm_mode = True
