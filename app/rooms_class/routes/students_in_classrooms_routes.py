from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
import uuid
from app.rooms_class.models.students_in_rooms_models import Student_Classrooms
from app.database.database import get_db
from app.schemas.schemas import Student_In_Section_Schema
from app.middleware import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/classrooms",
    tags=["Classrooms"],
    responses={404: {"description": "Not found"}}
)

# create a route to insert a student into a classroom
@router.post("/", status_code=status.HTTP_201_CREATED, response_description="Save a student into a classroom")
async def create_student_classroom(student_classroom: Student_Classrooms, db: Session = Depends(get_db),
                              current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    student_exists = db.query(Student_In_Section_Schema).filter(Student_In_Section_Schema.student_id == 
                                                                student_classroom.student_id).first()
    
    # if the student exists in the database, raise an exception
    if student_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Student already exists in the classroom")
    
    new_student = Student_In_Section_Schema(**student_classroom.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "Student added to classroom"}


# create a route to remove a student from a classroom
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, response_description="Remove a student from a classroom")
async def remove_student_classroom(student_id: uuid.UUID, db: Session = Depends(get_db),
                                    current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    student_exists = db.query(Student_In_Section_Schema).filter(Student_In_Section_Schema.student_id == student_id).first()
    
    # if the student doesn't exist in the database, raise an exception
    if not student_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Student doesn't exist in the classroom")
    
    db.delete(student_exists)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)