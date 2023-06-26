from fastapi import APIRouter, status, HTTPException, Depends, Request
from sqlalchemy.orm import Session, joinedload
import uuid
from typing import Optional
from app.students.models.students_models import Student_Create, Student_Response, All_Students
from app.database.database import get_db
from app.schemas.schemas import Student_Schema, Person_Schema, Academic_Degree_Schema, Institution_Schema, User_Schema
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


# define a route to get all students
@router.get("/", response_description="Get all students", response_model=list[All_Students],
            status_code=status.HTTP_200_OK)
def get_students(db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to perform this action")
    
    result = []

    try:
        students = db.query(Student_Schema).options(joinedload(Student_Schema.person)
                        ).join(Person_Schema, Student_Schema.person_id == Person_Schema.id, isouter=True
                        ).filter(Person_Schema.firstname.like(f"%{search}%")).limit(limit).offset(skip).all()

        if students == []:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No students found")
        
        # loop through the students and append them to the result list
        for student in students:
            user_data = {
                "id": student.id,
                "identification": student.identification,
                "contact": student.contact,
                "level_id": student.level_id,
                "observations": student.observations,
                "firstname": student.person.firstname,
                "lastname": student.person.lastname,
                "address": student.person.address,
                "phone": student.person.phone,
                "institution_id": student.person.institution_id,
            }

            result.append(user_data)
        
        # return the result list
        return result
    except Exception as e:
        print(str(e))


# define a route to get a student by id
@router.get("/{id}", response_description="Get a student by id", response_model=Student_Response,
            status_code=status.HTTP_200_OK)
async def get_student(id: str, db: Session = Depends(get_db)):
    student = db.query(Student_Schema).options(joinedload(Student_Schema.person)
                        ).join(Academic_Degree_Schema, Student_Schema.level_id == Academic_Degree_Schema.id, isouter=True
                        ).join(Person_Schema, Student_Schema.person_id == Person_Schema.id, isouter=True
                        ).join(Institution_Schema, Person_Schema.institution_id == Institution_Schema.id, isouter=True
                        ).join(User_Schema, User_Schema.id == Student_Schema.user_id, isouter=True
                        ).filter(Student_Schema.id == id).first()
    # if the student does not exist, raise an exception
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Student not found")
    # create a new dictionary to store the student data
    user_data = {
                "id": student.id,
                "firstname": student.person.firstname,
                "lastname": student.person.lastname,
                "address": student.person.address,
                "phone": student.person.phone,
                "institution_id": student.person.institution_id,
                "institution_name": student.person.institution.name,
                "level_id": student.level_id,
                "level_name": student.level.name,
                "contact": student.contact,
                "observations": student.observations,
                "person_id": student.person_id,
                "identification": student.identification,
                "user_id": student.user_id,
                "created_by": f"{student.user.person.firstname} {student.user.person.lastname}",
            }
    
    return user_data


# define a route to get a student by identification
@router.get("/{identification}/identification", response_description="Get a student by identification (DNI)", 
            response_model=Student_Response, status_code=status.HTTP_200_OK)
async def get_student(identification: str, db: Session = Depends(get_db)):
    student = db.query(Student_Schema).options(joinedload(Student_Schema.person)
                        ).join(Academic_Degree_Schema, Student_Schema.level_id == Academic_Degree_Schema.id, isouter=True
                        ).join(Person_Schema, Student_Schema.person_id == Person_Schema.id, isouter=True
                        ).join(Institution_Schema, Person_Schema.institution_id == Institution_Schema.id, isouter=True
                        ).join(User_Schema, User_Schema.id == Student_Schema.user_id, isouter=True
                        ).filter(Student_Schema.identification == identification).first()
    # if the student does not exist, raise an exception
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Student not found")
    # create a new dictionary to store the student data
    user_data = {
                "id": student.id,
                "firstname": student.person.firstname,
                "lastname": student.person.lastname,
                "address": student.person.address,
                "phone": student.person.phone,
                "institution_id": student.person.institution_id,
                "institution_name": student.person.institution.name,
                "level_id": student.level_id,
                "level_name": student.level.name,
                "contact": student.contact,
                "observations": student.observations,
                "person_id": student.person_id,
                "identification": student.identification,
                "user_id": student.user_id,
                "created_by": f"{student.user.person.firstname} {student.user.person.lastname}",
            }
    
    return user_data


# define a route to update a student
@router.put("/{id}", response_description="Update a student",
            status_code=status.HTTP_200_OK)
async def update_student(id: uuid.UUID, request: Request, db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to perform this action")
    
    # Creates an instance of the database engine and a session
    student_exists = db.query(Student_Schema).get(id)

    # if the user is not found, raise an exception
    if not student_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")

    # Parse the data in the body of the request
    updated_data = await request.json()

    # Update the fields provided in the request body
    for field, value in updated_data.items():
        if hasattr(student_exists, field):
            setattr(student_exists, field, value)
        elif hasattr(student_exists.person, field):
            setattr(student_exists.person, field, value)

    db.commit()
    db.refresh(student_exists)

    return {"message": "Student updated successfully"}