from pydantic import BaseModel
from typing import Optional
import uuid

# create a class for the model
class Level_Create(BaseModel):
    name: str

class LevelResponse(Level_Create):
    id: uuid.UUID
    class Config:
        orm_mode = True