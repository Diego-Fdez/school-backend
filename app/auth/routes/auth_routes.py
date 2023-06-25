from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.auth.models.auth_models import LoginResponse
from app.database.database import get_db
from app.schemas.schemas import User_Schema, Person_Schema
from app.utils.jwt_token import verify
from app.middleware import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/login",
    tags=["Login"],
    responses={404: {"description": "Not found"}}
)

# function to login a user
@router.post("/", response_description="Login a user", response_model=LoginResponse, status_code=status.HTTP_202_ACCEPTED)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User_Schema).join(Person_Schema, User_Schema.person_id == Person_Schema.id, isouter=True
                                    ).filter(User_Schema.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid password")
    
    # create a response object
    user_response = {
        "id": user.id,
        "firstname": user.person.firstname,
        "lastname": user.person.lastname,
        "institution_id": user.person.institution_id,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
        "is_teacher": user.is_teacher
    }
    
    #create a token
    access_token = oauth2.create_access_token(data={"user_id": str(user.id)})

    return {"access_token": access_token, "user": user_response, "token_type": "bearer"}