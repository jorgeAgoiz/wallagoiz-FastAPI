from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import Table
from config.db import Base, meta
from sqlalchemy import Column, Integer, String

userDB = Table('user', meta,
               Column('id', Integer, primary_key=True, nullable=False),
               Column('email', String, nullable=False),
               Column('password', String, nullable=False))
# user Table in MariaDB wallagoiz database
