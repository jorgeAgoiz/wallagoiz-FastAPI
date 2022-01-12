import sqlalchemy
import os
from dotenv import load_dotenv
from starlette.status import HTTP_201_CREATED
from utils.user import get_current_user
from utils.article import create_new_article
from models.article import Article
from config.db import engine, SessionLocal
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from models import article


load_dotenv()  # Variables de entorno
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
    new_article: Article = create_new_article(user_id, article, db)
    return new_article


# Continuaré aqui creando las nuevas rutas, el manejo de errores y los modelos de respuesta
