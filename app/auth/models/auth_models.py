from pydantic import BaseModel
import uuid
from app.users.models.users_models import User_Response

# creating a model for the login
class Login(BaseModel):
    username: str
    password: str

# create a model for the token
class TokenData(BaseModel):
    id: uuid.UUID

# create a model for the login response
class LoginResponse(BaseModel):
    access_token: str
    user: User_Response
    token_type: str