from fastapi import APIRouter, status, HTTPException, Depends, Request
from sqlalchemy.orm import Session, joinedload
import uuid
from typing import Optional
from app.students.models.students_models import Student_Create, Student_Response, Student_Update
from app.database.database import get_db
from app.schemas.schemas import Student_Schema, Person_Schema
from app.middleware import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"],
    responses={404: {"description": "Not found"}}
)

# define a route to create a student
@router.post("/", response_description="Create a new student", status_code=status.HTTP_201_CREATED)
def create_student(student: Student_Create, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to perform this action")
    
    try:
        # check if the student already exists
        student_exists = db.query(Student_Schema).filter(Student_Schema.identification == student.identification).first()
    
        # if the student exists, raise an exception
        if student_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"Student with identification {student.identification} already exists")
    
        # create a new dictionary to store the person data
        person_to_dict = {
        "firstname": student.firstname,
        "lastname": student.lastname,
        "address": student.address,
        "phone": student.phone,
        "institution_id": student.institution_id,
        }

        # save the person data to the database
        new_person = Person_Schema(**person_to_dict)

        db.add(new_person)
        db.commit()
        db.refresh(new_person)

        # create a new dictionary to store the student data
        student_to_dict = {
        "identification": student.identification,
        "contact": student.contact,
        "level_id": student.level_id,
        "user_id": current_user.id,
        "observations": student.observations,
        "person_id": new_person.id, 
        }

        # save the student data to the database
        new_student = Student_Schema(**student_to_dict)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return {"message": "Student created successfully",}
    except Exception as e:
        db.rollback()
        print(str(e))