from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from config.db import Base
from pydantic.main import BaseModel
from typing import Optional


class CreateFav(BaseModel):
    articleId: int
    userId: Optional[int]

    class Config:
        orm_mode = True


class FavsDB(Base):
    __tablename__ = 'fav'

    userId = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    articleId = Column(Integer, ForeignKey(
        "article.id", ondelete="CASCADE"), primary_key=True, nullable=False)

    articles = relationship(
        "ArticleDB", back_populates="user_favs")
    users = relationship("UserDB", back_populates="favs")
