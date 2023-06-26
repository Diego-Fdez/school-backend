from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from app.levels.models.levels_models import Level_Create, LevelResponse
from app.database.database import get_db
from app.schemas.schemas import Academic_Degree_Schema
from app.middleware import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/levels",
    tags=["Academic Degree"],
    responses={404: {"description": "Not found"}}
)

# define a route to create a new academic degree
@router.post("/", response_description="Create a new academic degree", status_code=status.HTTP_201_CREATED, 
              response_model=LevelResponse)
async def create_academic_degree(level: Level_Create, db: Session = Depends(get_db), 
                            current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # create a new academic degree
    new_level = Academic_Degree_Schema(**level.dict())
    db.add(new_level)
    db.commit()
    db.refresh(new_level)
    return new_level

# define a route to get all academic degrees
@router.get("/", response_description="Get all academic degrees", status_code=status.HTTP_200_OK,
              response_model=list[LevelResponse])
async def get_all_academic_degrees(db: Session = Depends(get_db),
                                    current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # get all academic degrees
    academic_degrees = db.query(Academic_Degree_Schema).all()

    # if academic degrees are not found
    if academic_degrees == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Academic degrees not found")
    
    return academic_degrees

# define a route to update an academic degree

@router.patch("/{id}", response_description="Update an academic degree", status_code=status.HTTP_200_OK,
              response_model=LevelResponse)
async def update_academic_degree(id: uuid.UUID, level: Level_Create, db: Session = Depends(get_db),
                                    current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser) | (not current_user.is_teacher):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # get academic degree
    academic_degree = db.query(Academic_Degree_Schema).filter(Academic_Degree_Schema.id == id).first()

    # if academic degree is not found
    if academic_degree == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Academic degree not found")
    
    # update academic degree
    academic_degree.name = level.name
    db.commit()
    db.refresh(academic_degree)
    return academic_degree