from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from typing import Optional
from app.school_period.models.school_period_models import SchoolPeriod, SchoolPeriodResponse
from app.database.database import get_db
from app.schemas.schemas import Period_Schema
from app.middleware import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/periods",
    tags=["School Periods"],
    responses={404: {"description": "Not found"}}
)

# define a route to create a new school period
@router.post("/", response_model=SchoolPeriodResponse, response_description="Create a new school period", 
              status_code=status.HTTP_201_CREATED)
async def create_school_period(period: SchoolPeriod, db: Session = Depends(get_db), 
                          current_user: int = Depends(oauth2.get_current_user)):
    # check if the current user is an admin or superuser
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform this action")
    
    # create a new school period
    new_period = Period_Schema(**period.dict())
    db.add(new_period)
    db.commit()
    db.refresh(new_period)
    return new_period


# define a route to get all school periods
@router.get("/", response_model=list[SchoolPeriodResponse], response_description="Get all school periods",
              status_code=status.HTTP_200_OK)
async def get_all_school_periods(db: Session = Depends(get_db), search: Optional[str] = ""):
    # get all school periods
    periods = db.query(Period_Schema).filter(Period_Schema.name.ilike(f"%{search}%")).all()

    # if no school periods found
    if not periods:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No school periods found")
    
    return periods


#define a route to get a school period by id
@router.get("/{period_id}", response_model=SchoolPeriodResponse, response_description="Get a school period by id",
              status_code=status.HTTP_200_OK)
async def get_school_period_by_id(period_id: str, db: Session = Depends(get_db)):
    # get a school period by id
    period = db.query(Period_Schema).filter(Period_Schema.id == period_id).first()

    # if no school period found
    if not period:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No school period with id {period_id} found")

    return period


# define a route to update a school period
@router.patch("/{period_id}", response_model=SchoolPeriodResponse, response_description="Update a school period",
              status_code=status.HTTP_200_OK)
async def update_school_period(period_id: uuid.UUID, period: SchoolPeriod, db: Session = Depends(get_db),
                                current_user: int = Depends(oauth2.get_current_user)):
    # check if the current user is an admin or superuser
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform this action")
    
    # get a school period by id
    period_to_update = db.query(Period_Schema).filter(Period_Schema.id == period_id).first()

    # if no school period found
    if not period_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No school period with id {period_id} found")

    # update a school period
    period_to_update.name = period.name
    period_to_update.user_id = current_user.id
    
    db.commit()
    db.refresh(period_to_update)
    return period_to_update