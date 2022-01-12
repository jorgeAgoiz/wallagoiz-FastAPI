import sqlalchemy
import os
from dotenv import load_dotenv
from config.db import engine, SessionLocal
from fastapi import APIRouter
from models import favs


load_dotenv()  # Variables de entorno

favs.Base.metadata.create_all(bind=engine)

fav = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
