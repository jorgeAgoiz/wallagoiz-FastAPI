from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str


app = FastAPI()
# Comienzo a montar el servidor


@app.get('/signup')
async def root():
    return {'message': 'Hello World!!'}


@app.post('/signin')
async def signin(user: User):
    print(user)
    return {'data': user}
