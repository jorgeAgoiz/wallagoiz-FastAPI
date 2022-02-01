from ntpath import join
from pprint import pprint
from models.article import ArticleDB
from models.favs import FavsDB
from models.user import UserDB
from sqlalchemy.orm.session import Session


def get_favs_from(user_id: int, db: Session):
    return db.query(
        FavsDB.articleId,
        ArticleDB.title,
        ArticleDB.description,
        ArticleDB.price,
        ArticleDB.category,
        ArticleDB.picture,
        ArticleDB.created_at,
        UserDB.id
    ).join(FavsDB, FavsDB.userId == UserDB.id).join(
        ArticleDB, ArticleDB.id == FavsDB.articleId).filter(UserDB.id == user_id).all()
