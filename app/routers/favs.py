from pprint import pprint
from typing import List
import sqlalchemy
import os
from dotenv import load_dotenv
from fastapi.params import Depends
from utils.fav import delete_fav
from utils.fav import create_fav
from utils.fav import get_favs_from
from models.article import Article
from models.favs import CreateFav
from utils.user import get_current_user
from config.db import engine, SessionLocal
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
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


@fav.post("/favs", status_code=HTTP_201_CREATED, response_model=CreateFav)
def create_new_favs(fav: CreateFav, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    try:
        fav.userId = user_id
        new_fav = create_fav(fav, db)
        return new_fav
    except:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Something went wrong.")


@fav.get("/favs", status_code=HTTP_200_OK)
def get_favs(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    favs_articles: List[Article] = get_favs_from(user_id, db)

    if len(favs_articles) == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Does not exists articles.")
    return favs_articles


@fav.delete("/favs/{article_id}", status_code=HTTP_204_NO_CONTENT)
def remove_fav(article_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    fav_removed: int = delete_fav(article_id, user_id, db)

    if fav_removed == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="This article does not exist.")
    return
