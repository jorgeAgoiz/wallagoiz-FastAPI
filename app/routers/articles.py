from pprint import pprint
from typing import List, Optional
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Query
from sqlalchemy.sql.functions import user
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from models.article import UpdateArticle
from utils.article import update_article
from utils.article import get_article_by_userId, get_article_by_category, get_article_by_id, remove_article, get_articles
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


@article.get("/article", response_model=Article | List[Article], status_code=HTTP_200_OK)
def get_article_by(
    id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    if id:  # Artículo específico
        article: Article = get_article_by_id(id, db)
        if article == None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                                detail="Article not found.")
        return article
    elif category:  # Artículos por categoria
        articles: List[Article] = get_article_by_category(category, db)
        if len(articles) == 0:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                                detail="Does not exists articles.")
        return articles
    else:  # Si no hay ninguna queries, todos los articulos del usuario
        articles: List[Article] = get_article_by_userId(user_id, db)
        if len(articles) == 0:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                                detail="Does not exists articles.")
        # Quizá aquí deba modificar esto para llamar todos los articulos de otro usuario
        return articles


@article.get("/articles", response_model=List[Article], status_code=HTTP_200_OK)
def get_all_articles(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    articles: List[Article] = get_articles(db)
    if len(articles) == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Does not exists articles.")
    return articles


@article.delete("/article/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_article(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    article: int = remove_article(id, user_id, db)

    if article == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="This article does not exist.")
    return


@article.patch("/article/{id}", response_model=Article, status_code=HTTP_200_OK)
def updt_article(id: int, article: UpdateArticle, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return update_article(id, article, db)
    # Este endpoint habra que modificarlo porque deberemos subir la imagen a un bucket
