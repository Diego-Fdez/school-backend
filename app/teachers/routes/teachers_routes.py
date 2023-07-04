from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
import uuid
from app.teachers.models.teachers_models import Teachers_Create, Teachers_Response
from app.database.database import get_db
from app.schemas.schemas import Teacher_Schema
from app.middleware import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/teachers",
    tags=["Teachers"],
    responses={404: {"description": "Not found"}}
)

# add a new teacher to students
@router.post("/", response_description="Add a new teacher to students", status_code=status.HTTP_201_CREATED,
              response_model=Teachers_Response)
async def add_teacher(body: Teachers_Create, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    new_student = Teacher_Schema(**body.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "id": new_student.id,
        "student_id": new_student.student_id,
        "teacher_id": new_student.teacher_id,
        "teacher": f"{new_student.teacher.person.firstname} {new_student.teacher.person.lastname}",
    }


# remove a teacher from students
@router.delete("/{id}", response_description="Remove a teacher from students", status_code=status.HTTP_204_NO_CONTENT)
async def remove_teacher(id: uuid.UUID, db: Session = Depends(get_db),
                          current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    query = db.query(Teacher_Schema).filter(Teacher_Schema.id == id).first()
    
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"This id {id} does not exist")
    
    db.delete(query)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)