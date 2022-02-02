from models.article import ArticleDB
from models.favs import FavsDB, CreateFav
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


def create_fav(fav: CreateFav, db: Session):
    new_fav = FavsDB(**fav.dict())
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)
    return new_fav


def delete_fav(article_id: int, user_id: int, db: Session):
    fav = db.query(FavsDB).filter_by(
        userId=user_id, articleId=article_id).delete(synchronize_session=False)
    db.commit()
    return fav
