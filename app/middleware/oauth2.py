from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.schemas.schemas import User_Schema
from app.database.database import get_db
from app.config.configs import settings
from app.auth.models.auth_models import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

#expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Secret_key
SECRET_KEY = settings.secret_key

#algorithm
ALGORITHM = settings.algorithm

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(User_Schema).filter(User_Schema.id == token.id).first()
    
    return user