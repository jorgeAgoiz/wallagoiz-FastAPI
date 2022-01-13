from typing import List, Optional
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Query
from sqlalchemy.sql.functions import user
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from utils.article import get_article_by
from utils.article import remove_article
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


@article.get("/article", response_model=Article | List[Article], status_code=HTTP_200_OK)
def get_article_by_ids(
    id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    if id == None:
        print(f"The user id is {user_id}")
    else:
        print(f"The id of the article is {id}")
    # article: Article = get_article_by(id, db)
    # if article == None:
    #     raise HTTPException(status_code=HTTP_404_NOT_FOUND,
    #                         detail="Article not found.")
    # return article

    # Continuare aquí rediseñando este endpoint


@article.get("/article", response_model=List[Article], status_code=HTTP_200_OK)
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


@article.get("/article-prueba")
def probando_queries(
    user_id: Optional[str] = Query(None),
    id: Optional[str] = Query(None)
):

    prueba = {"userId": user_id, "name": name}

    # estoy manejando las queries, implementaré mejor queries que params
    print(prueba)
