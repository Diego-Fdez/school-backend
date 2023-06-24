from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.institutions.models.institutions_models import Institution_Base, Institution_Response
from app.database.database import get_db
from app.schemas.schemas import Institution_Schema

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/institutions",
    tags=["Institutions"],
    responses={404: {"description": "Not found"}}
)

# define a route to create a new institution
@router.post("/", response_description="Create a new institution", response_model=Institution_Response, 
              status_code=status.HTTP_201_CREATED)
def create_institution(institution: Institution_Base, db: Session = Depends(get_db)):
    institution_exists =  db.query(Institution_Schema).filter(Institution_Schema.name == institution.name).first()

    if institution_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"Institution {institution.name} already exists")
    
    new_institution = Institution_Schema(**institution.dict())
    db.add(new_institution)
    db.commit()
    db.refresh(new_institution)
    return new_institution