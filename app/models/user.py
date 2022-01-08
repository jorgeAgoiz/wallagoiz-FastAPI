from datetime import date, datetime
from typing import Optional
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from config.db import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String


class CreateUser(BaseModel):  # Usuario para crear
    id: Optional[int]
    email: str
    password: str
    name: str
    lastName: str
    location: str
    birthday: Optional[str]
    gender: Optional[str]
    profilePic: Optional[str]
    created_at: Optional[date]

    class Config:
        orm_mode = True


class UserDB(Base):  # Table user in MariaDB
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    location = Column(String(100), nullable=False)
    birthday = Column(String(100), nullable=True)
    gender = Column(String(50), nullable=True)
    profilePic = Column(String(1200), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
