from sqlalchemy.orm.session import Session
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from models.article import UpdateArticle
from models.article import ArticleDB
from models.article import Article


def create_new_article(user_id: int, article: Article, db: Session):
    article.userId = user_id
    new_article = ArticleDB(**article.dict())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def get_articles(db: Session):
    return db.query(ArticleDB).all()


def get_article_by_id(id: int, db: Session):
    return db.query(ArticleDB).filter_by(id=id).first()


def get_article_by_userId(user_id: int, db: Session):
    return db.query(ArticleDB).filter_by(userId=user_id).all()


def get_article_by_category(category: str, db: Session):
    return db.query(ArticleDB).filter_by(category=category).all()


def remove_article(id: int, user_id: int, db: Session):
    article = db.query(ArticleDB).filter_by(
        userId=user_id, id=id).delete(synchronize_session=False)
    db.commit()
    return article


def update_article(id: int, article: UpdateArticle, db: Session):
    new_data = article.dict(exclude_unset=True, exclude_none=True)
    article_to = db.query(ArticleDB).filter_by(id=id)

    if article_to.first() == None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Article not found.')

    article_to.update(new_data, synchronize_session=False)
    db.commit()
    return article_to.first()
