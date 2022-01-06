from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from models.user import CreatedUser
from models.user import CreateUser
from models.user import UserDB

# User Functions


def get_all_users(db: Session, skip: int, limit: int):
    return db.query(UserDB).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, id: int):
    return db.query(UserDB).filter_by(id=id).first()

# Imposible hacerla funcionar RecursionError: maximum recursion depth exceeded
# def create_user(user: CreateUser, db: Session):
#     new_user = UserDB(email=user.email, password=user.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
