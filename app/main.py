from fastapi import FastAPI
from routers.users import user

app = FastAPI()

app.include_router(user)
