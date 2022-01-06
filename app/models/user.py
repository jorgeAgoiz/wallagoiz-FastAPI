from datetime import datetime
from typing import Optional
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from config.db import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String


class User(BaseModel):  # User Schema
    id: int
    email: str
    password: str
    created_at: datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: str
    password: str


class CreatedUser(CreateUser):
    id: Optional[int]
    created_at: Optional[str]


class UserDB(Base):  # Table user in MariaDB
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
