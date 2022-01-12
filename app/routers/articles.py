from typing import List
from fastapi.exceptions import HTTPException
from sqlalchemy.sql.functions import user
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from utils.article import get_article
from utils.article import get_articles
from utils.user import get_current_user
from utils.article import create_new_article
from models.article import Article
from config.db import engine, SessionLocal
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from models import article

article.Base.metadata.create_all(bind=engine)

article = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@article.post("/article", response_model=Article, status_code=HTTP_201_CREATED)
def create_article(article: Article, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    try:
        new_article: Article = create_new_article(user_id, article, db)
        return new_article
    except:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Something went wrong.")


@article.get("/article")
def get_all_articles(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    articles: List[Article] = get_articles(db)
    if len(articles) == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Does not exists articles.")
    return articles


@article.get("/article/{id}")
def get_article_by_id(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    article: Article = get_article(id, db)
    if article == None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Article not found.")
    return article


# Continuaré aqui creando las nuevas rutas, el manejo de errores y los modelos de respuesta
