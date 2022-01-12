from sqlalchemy.orm.session import Session
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


def get_article(id: int, db: Session):
    return db.query(ArticleDB).filter_by(id=id).first()
