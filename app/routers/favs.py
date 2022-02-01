from typing import List
import sqlalchemy
import os
from dotenv import load_dotenv
from fastapi.params import Depends
from utils.fav import get_favs_from
from models.article import Article
from models.favs import CreateFav
from utils.user import get_current_user
from config.db import engine, SessionLocal
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from fastapi import APIRouter, HTTPException
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
    # Implementar crear fav


@fav.get("/favs", status_code=HTTP_200_OK)
def get_favs(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    favs_articles: List[Article] = get_favs_from(user_id, db)
    if len(favs_articles) == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Does not exists articles.")
    return favs_articles


@fav.delete("/fav")
def remove_fav(article_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return "Hello Motherfuckers"
    # Implementar eliminar fav
