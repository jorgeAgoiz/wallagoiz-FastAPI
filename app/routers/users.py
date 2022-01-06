from sqlalchemy.sql.expression import null
from config.db import engine, SessionLocal
from typing import List
from fastapi import APIRouter, Response, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from models.user import User
from models import user
from utils.user import get_all_users, get_user_by_id

user.Base.metadata.create_all(bind=engine)

user = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# With connection to DB.wallagoiz
@user.get('/users')
async def get_users(response: Response, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users: List = get_all_users(db, skip=skip, limit=limit)
    if len(users) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Users not found'}
    return users


@user.get('/users/{id}')
async def get_user_with(id: int, response: Response, db: Session = Depends(get_db)):
    user = get_user_by_id(db, id)
    if user == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'User not found'}
    else:
        return user

# @user.post('/users', status_code=status.HTTP_201_CREATED)
# async def create_user(user: User):

#     user_new = user.dict()
#     result = conn.execute(userDB.insert().values(user_new))

#     new_user = conn.execute(userDB.select().where(
#         userDB.c.id == result.lastrowid)).first()
#     return {'New user': new_user}


# @user.delete('/users/{id}')
# async def delete_user(id: int, response: Response):
#     user_index = find_index_user(id)
#     if user_index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'User with {id} ID, was not found.')
#     else:
#         users.pop(user_index)
#         return {"Users": users}
