import sqlalchemy
import os
from dotenv import load_dotenv
from fastapi.params import Depends
from models.favs import CreateFav
from utils.user import get_current_user
from config.db import engine, SessionLocal
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_201_CREATED
from fastapi import APIRouter
from models import favs


load_dotenv()  # Variables de entorno

favs.Base.metadata.create_all(bind=engine)

fav = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@fav.post("/fav", status_code=HTTP_201_CREATED)
def create_fav(fav: CreateFav, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return {"userId": user_id, "articleId": fav.article_id}
    # Seguir aquí implementando metodos fav
