from sqlalchemy.orm.session import Session
from models.user import UserDB


def get_all_users(db: Session, skip: int, limit: int):
    return db.query(UserDB).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, id: int):
    return db.query(UserDB).filter_by(id=id).first()
