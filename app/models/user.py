from config.db import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

# Esto podría ir en una carpeta Schemas


class User(BaseModel):
    id: int
    email: str
    password: str

    class Config:
        orm_mode = True


class UserDB(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
