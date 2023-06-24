from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from typing import Optional
from app.users.models.users_models import User_Create, User_Response, User_Update
from app.database.database import get_db
from app.schemas.schemas import User_Schema, Person_Schema

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

#route and function to create a new user
@router.post("/", response_description="Create a new user", 
                status_code=status.HTTP_201_CREATED)
async def create_user(user: User_Create, db: Session = Depends(get_db)):
    try:
        # check if the user already exists
        user_exists = db.query(User_Schema).filter(User_Schema.email == user.email).first()
    
        # if the user exists, raise an exception
        if user_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {user.email} already exists")
    
        # create a new dictionary to store the person data
        person_to_dict = {
        "firstname": user.firstname,
        "lastname": user.lastname,
        "address": user.address,
        "phone": user.phone,
        "institution_id": user.institution_id,
        }

        # save the person data to the database
        new_person = Person_Schema(**person_to_dict)

        db.add(new_person)
        db.commit()
        db.refresh(new_person)

        # create a new dictionary to store the user data
        user_to_dict = {
        "email": user.email,
        "password": user.password,
        "person_id": new_person.id, 
        }

        # save the user data to the database
        new_user = User_Schema(**user_to_dict)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created successfully",}
    except Exception as e:
        db.rollback()
        print(str(e))
    finally:
        db.close()