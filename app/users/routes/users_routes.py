from fastapi import APIRouter, status, HTTPException, Depends, Request
from sqlalchemy.orm import Session, joinedload
import uuid
from typing import Optional
from app.users.models.users_models import User_Create, User_Response, User_Update
from app.database.database import get_db
from app.schemas.schemas import User_Schema, Person_Schema
from app.utils.jwt_token import hash
from app.middleware import oauth2

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

        #hash the password - user.password
        hashed_pwd = hash(user.password)

        # create a new dictionary to store the user data
        user_to_dict = {
        "email": user.email,
        "password": hashed_pwd,
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

# create a function to get all users
@router.get("/", response_description="Get all users", response_model=list[User_Response], status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="You are not authorized to perform this action")
        
    result = []

    # Creates an instance of the database engine and a session
    users = db.query(User_Schema).options(joinedload(User_Schema.person)).limit(limit).offset(skip).all()

    # if the users are not found, raise an exception
    if users == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
        
    # loop through the users and append them to the result list
    for user in users:
        user_data = {
            "id": user.id,
            "email": user.email,
            "firstname": user.person.firstname,
            "lastname": user.person.lastname,
            "address": user.person.address,
            "phone": user.person.phone,
            "institution_id": user.person.institution_id,
            "is_superuser": user.is_superuser,
            "is_admin": user.is_admin,
            "is_teacher": user.is_teacher
        }
        result.append(user_data)
        
    # return the result list
    return result

#get a single user by id
@router.get("/{id}", response_description="Get a single user", 
            response_model=User_Response, status_code=status.HTTP_200_OK)
async def get_user(id: uuid.UUID, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="You are not authorized to perform this action")
        
    # Creates an instance of the database engine and a session
    user = db.query(User_Schema).options(joinedload(User_Schema.person)).filter(User_Schema.id == id).first()

    # if the user is not found, raise an exception
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
        
    # create a dictionary to store the user data
    user_data = {
        "id": user.id,
        "email": user.email,
        "firstname": user.person.firstname,
        "lastname": user.person.lastname,
        "address": user.person.address,
        "phone": user.person.phone,
        "institution_id": user.person.institution_id,
        "is_superuser": user.is_superuser,
        "is_admin": user.is_admin,
        "is_teacher": user.is_teacher
    }
        
    # return the result list
    return user_data

# function to update a user
@router.patch("/{id}", response_description="Update a user", status_code=status.HTTP_200_OK)
async def update_user(id: uuid.UUID, request: Request, user: User_Update, db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    # Creates an instance of the database engine and a session
    user_exists = db.query(User_Schema).get(id)

    # if the user is not found, raise an exception
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    if (not current_user.is_superuser) | (current_user.id != user_exists.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="You are not authorized to perform this action")
    # Parse the data in the body of the request
    datos_actualizados = await request.json()

    # Update the fields provided in the request body
    for campo, valor in datos_actualizados.items():
        if hasattr(user_exists, campo):
            setattr(user_exists, campo, valor)
        elif hasattr(user_exists.person, campo):
            setattr(user_exists.person, campo, valor)

    # Update the password and hash it
    if user.password:
        user_exists.password = hash(user.password)

    db.commit()
    db.refresh(user_exists)

    return {"message": "User updated successfully"}