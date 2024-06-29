from pydantic import BaseModel, EmailStr, constr
from sqlalchemy import Column, Integer, String, Boolean


# User database
# Dummy user data
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$KIXTOG3.YHbKtN6Uw1n/ue/W.c/7uOHmpxE8v.7zYy0D.1QXqZ.ea", # "password"
        "disabled": False,
    }
}


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    # password: constr(min_length=8)
    user_role: str
    username: str
    email:str
    status: str = "pending"
    password: constr(min_length=4)
    # id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, unique=True, index=True)
    # email = Column(String, unique=True, index=True)
    # hashed_password = Column(String)
    # user_role = Column(String)
    # status = Column(String, default="pending")

    # id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, unique=True, index=True)
    # email = Column(String, unique=True, index=True)
    # hashed_password = Column(String)
    # user_role = Column(String)
    # status = Column(String, default="pending")

class UserResponse(UserBase):
    id: int
    user_role: str
    status: str
    username:str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class UserInDB(UserBase):
    hashed_password: str    
