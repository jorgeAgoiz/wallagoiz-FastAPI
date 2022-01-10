import sqlalchemy
import os
from dotenv import load_dotenv
from datetime import timedelta
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE
from utils.user import get_current_user
from utils.user import authenticate_user
from utils.oauth2 import create_access_token
from models.token import Token
from models.user import UserSignIn
from models.user import CreateUser
from config.db import engine, SessionLocal
from typing import List
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from models import user
from utils.user import get_all_users, get_user_by_id, create_new_user


load_dotenv()  # Variables de entorno para JWT
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

user.Base.metadata.create_all(bind=engine)
user = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user.get('/users', response_model=List[CreateUser], status_code=HTTP_200_OK)
def get_users(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    users: List[CreateUser] = get_all_users(db)
    if len(users) == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Does not exists users.")
    return users


@user.get('/users/{id}', response_model=CreateUser, status_code=HTTP_200_OK)
def get_user_with(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    user: CreateUser = get_user_by_id(db, id)
    if user == None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="User not found.")
    else:
        return user


@user.post('/signup', response_model=CreateUser, status_code=HTTP_201_CREATED)
def sign_up(user: CreateUser, db: Session = Depends(get_db)):
    try:
        result: CreateUser = create_new_user(user, db)
        return result
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail="Email is bussy.")


@user.post("/signin", status_code=HTTP_200_OK, response_model=Token)
def sign_in(user: UserSignIn, db: Session = Depends(get_db)):
    user_authenticated: CreateUser = authenticate_user(user, db)
    if not user_authenticated:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"user_id": user_authenticated.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
