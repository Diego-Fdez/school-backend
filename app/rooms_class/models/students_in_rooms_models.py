from pydantic import BaseModel
import uuid
from datetime import datetime

# create a model for the students in classrooms
class Student_Classrooms(BaseModel):
    section_id: uuid.UUID
    student_id: uuid.UUID
