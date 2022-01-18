from datetime import date
from typing import Optional
from pydantic.main import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Float
from config.db import Base
from sqlalchemy import Column, Integer, String


class Article(BaseModel):
    id: Optional[int]
    userId: Optional[int]
    title: str
    description: str
    price: float
    category: str
    picture: str
    created_at: Optional[date]

    class Config:
        orm_mode = True


class UpdateArticle(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category: Optional[str]
    picture: Optional[str]


class ArticleDB(Base):
    __tablename__ = 'article'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    userId = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(1200), nullable=False)
    price = Column(Float(6, 2), nullable=False)
    category = Column(String(100), nullable=False)
    picture = Column(String(1200), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    author = relationship(
        "UserDB", back_populates="articles")
    user_favs = relationship("FavsDB", back_populates="articles")
