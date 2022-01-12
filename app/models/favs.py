from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from config.db import Base


class FavsDB(Base):
    __tablename__ = 'fav'
    favID = Column(Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    userId = Column(Integer, ForeignKey("user.id"), nullable=False)
    articleId = Column(Integer, ForeignKey("article.id"), nullable=False)

    articles = relationship("ArticleDB", back_populates="user_favs")
    users = relationship("UserDB", back_populates="favs")
