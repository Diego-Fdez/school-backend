from pydantic import BaseModel
import uuid

# create a pydantic model for school periods
class SchoolPeriod(BaseModel):
    name: str
    user_id: uuid.UUID

class SchoolPeriodResponse(SchoolPeriod):
    id: uuid.UUID
    class Config:
        orm_mode = True