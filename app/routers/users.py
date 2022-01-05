from fastapi import APIRouter, Response, status
from random import randrange
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from models.user import userDB
from config.db import conn

user = APIRouter()


class User(BaseModel):
    email: str
    password: str


# Variable to test my firsts endpoints without DataBase
users = [{"id": 1, "email": "probando@gmail.com", "password": "loquesea"},
         {"id": 2, "email": "otraprueba@gmail.com",
             "password": "loqueseaversiondos"},
         {"id": 3, "email": "yanoteacuerdas@gmail.com", "password": "loqueseaversiontres"}]


def find_index_user(id):
    for i, u in enumerate(users):
        if(u['id'] == id):
            print(i)
            return i


# With connection to DB.wallagoiz
@user.get('/users')
async def get_users():
    return conn.execute(userDB.select()).fetchall()


@user.get('/users/{id}')
async def get_user_with(id: int, response: Response):
    for user in users:
        print(user)
        if user['id'] == id:
            return {'Your user': user}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'message': 'User not found'}


@user.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    user_new = user.dict()
    user_new['id'] = randrange(0, 1000)
    print(user_new)
    users.append(user_new)
    return {'New user': user_new, 'All users': users}


@user.delete('/users/{id}')
async def delete_user(id: int, response: Response):
    user_index = find_index_user(id)
    if user_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with {id} ID, was not found.')
    else:
        users.pop(user_index)
        return {"Users": users}
