from pydantic import BaseModel
import uuid

# create a pydantic model for create institution
class Institution_Base(BaseModel):
    name: str

class Institution_Response(Institution_Base):
    id: uuid.UUID
    class Config:
        orm_mode = True