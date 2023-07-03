from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from typing import Optional
from app.subjects.models.subjects_models import Subject_Create, Subject_Response
from app.database.database import get_db
from app.schemas.schemas import Subject_Schema
from app.middleware import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/subjects",
    tags=["Subjects"],
    responses={404: {"description": "Not found"}}
)

# define the route for creating a new subject
@router.post("/", response_description="Create a new subject", status_code=status.HTTP_201_CREATED, 
                response_model=Subject_Response)
async def create_subject(subject: Subject_Create, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not authorized to perform this action")
    #save the subject to the database
    new_subject = Subject_Schema(**subject.dict())
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject


#define a route for getting all subjects
@router.get("/", response_description="Get all subjects", response_model=list[Subject_Response],
            status_code=status.HTTP_200_OK)
async def get_all_subjects(db: Session = Depends(get_db), search: Optional[str] = ""):
    subjects = db.query(Subject_Schema).filter(Subject_Schema.name.ilike(f"%{search}%")).all()

    #if no subjects are found, raise an exception
    if not subjects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No subjects found")
    
    return subjects


#define a route for getting a single subject
@router.get("/{subject_id}", response_description="Get a single subject by id", response_model=Subject_Response,
            status_code=status.HTTP_200_OK)
async def get_subject_by_id(subject_id: uuid.UUID, db: Session = Depends(get_db)):
    subject = db.query(Subject_Schema).filter(Subject_Schema.id == subject_id).first()

    #if no subject is found, raise an exception
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Subject with id {subject_id} not found")
    
    return subject


# define a route for updating a subject

@router.patch("/{subject_id}", response_description="Update a subject", response_model=Subject_Response,
            status_code=status.HTTP_200_OK)
async def update_subject(subject_id: uuid.UUID, subject: Subject_Create, db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not authorized to perform this action")
    
    subject_query = db.query(Subject_Schema).filter(Subject_Schema.id == subject_id)
    subject_query_result = subject_query.first()

    #if no subject is found, raise an exception
    if not subject_query_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Subject with id {subject_id} not found")
    
    subject_query.update(**subject.dict(), synchronize_session=False)
    db.commit()
    return subject_query.first()