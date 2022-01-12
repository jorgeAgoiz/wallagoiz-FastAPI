from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.users import user
from routers.articles import article
from routers.favs import fav

app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(article)
app.include_router(fav)
