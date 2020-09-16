from fastapi import Depends, APIRouter
import jwt
from sqlalchemy.orm import Session
from starlette.requests import Request
from pydantic import BaseModel
from db import User, engine, get_db
from typing import List

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    email: str
    hashed_password: str


class UserOut(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    encoded_password: str


@router.get("/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/login")
def auth_user(user: UserAuth,  db: Session = Depends(get_db)):
    decoded = jwt.decode(user.encoded_password,
                         'secret', algorithms='HS256')
    user = db.query(User).filter(
        User.hashed_password == decoded.password).first()
    return user


@router.post("/sign_up")
async def sign_up_user(user: UserCreate,  db: Session = Depends(get_db)):
    jwt_payload = {
        'email': user.email,
        'password': user.hashed_password
    }
    encoded_password = jwt.encode(jwt_payload, 'secret', algorithm='HS256')
    db_user = User(name=user.name, email=user.email,
                   hashed_password=encoded_password)
    db.add(db_user)
    db.commit()
