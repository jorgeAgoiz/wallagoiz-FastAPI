import sqlalchemy
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE
from models.user import CreateUser
from config.db import engine, SessionLocal
from typing import List
from fastapi import APIRouter, Response, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from models import user
from utils.user import get_all_users, get_user_by_id, create_new_user

user.Base.metadata.create_all(bind=engine)

user = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get All Users
@user.get('/users', response_model=List[CreateUser], status_code=HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users: List[CreateUser] = get_all_users(db, skip=skip, limit=limit)
    if len(users) == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Does not exists users.")
    return users

# Get specified user by ID


@user.get('/users/{id}', response_model=CreateUser, status_code=HTTP_200_OK)
def get_user_with(id: int, db: Session = Depends(get_db)):
    user: CreateUser = get_user_by_id(db, id)
    if user == None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="User not found.")
    else:
        return user

# Create user

# Necesario controlar el manejo de errores


@user.post('/users', response_model=CreateUser, status_code=HTTP_201_CREATED)
def sign_up(user: CreateUser, db: Session = Depends(get_db)):
    # Aqui vamos a implementar los JWT  y Hash en el password
    try:
        result: CreateUser = create_new_user(user, db)
        return result
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail="Email is bussy.")


# @user.delete('/users/{id}')
# async def delete_user(id: int, response: Response):
#     user_index = find_index_user(id)
#     if user_index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'User with {id} ID, was not found.')
#     else:
#         users.pop(user_index)
#         return {"Users": users}
