from fastapi import FastAPI
from random import randrange
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str


# Variable to test my firsts endpoints
users = [{"id": 1, "email": "probando@gmail.com", "password": "loquesea"},
         {"id": 2, "email": "otraprueba@gmail.com", "password": "loqueseaversiondos"}]

app = FastAPI()
# Comienzo a montar el servidor


@app.get('/users')
async def get_users():
    return users


@app.get('/users/{id}')
async def get_user_with(id: int):
    for user in users:
        print(user)
        if user['id'] == id:
            return {'Your user': user}
        else:
            return {'message': 'User not found'}


@app.post('/users')
async def create_user(user: User):
    user_new = user.dict()
    user_new['id'] = randrange(0, 1000)
    print(user_new)
    users.append(user_new)
    return {'New user': user_new, 'All users': users}
