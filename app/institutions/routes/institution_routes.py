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

# define a route to get all institutions
@router.get("/", response_description="Get all institutions", response_model=list[Institution_Response],
            status_code=status.HTTP_200_OK)
def get_all_institutions(db: Session = Depends(get_db), search: Optional[str] = ""):
    institutions = db.query(Institution_Schema).filter(Institution_Schema.name.like(f"%{search}%")).all()

    # if institutions is None, return an HTTPException
    if institutions == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No institutions found")
    
    return institutions

# define a route to get a single institution by id
@router.get("/{id}", response_description="Get a single institution by id", response_model=Institution_Response,
            status_code=status.HTTP_200_OK)
async def get_institution_by_id(id: int, db: Session = Depends(get_db)):
    institution = db.query(Institution_Schema).filter(Institution_Schema.id == id).first()

    # if institution is None, return an HTTPException
    if institution is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Institution with id {id} not found")
    
    return institution