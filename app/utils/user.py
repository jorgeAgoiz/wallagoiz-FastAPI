from typing import Optional
from sqlalchemy.orm.session import Session
from models.user import UserSignIn
from models.user import CreateUser
from models.user import UserDB
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from dotenv import load_dotenv


load_dotenv()  # Variables de entorno para JWT
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


# User Functions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)
    # Función para hashear el password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    # Esta función para el sign in, verificación de password


def get_all_users(db: Session, skip: int, limit: int):
    return db.query(UserDB).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, id: int):
    return db.query(UserDB).filter_by(id=id).first()


def create_new_user(user: CreateUser, db: Session):
    user.password = get_password_hash(user.password)
    new_user = UserDB(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user  # Sign Up Function


def sign_in_user(user_to_auth: UserSignIn, db: Session):
    email = user_to_auth.email
    plain_password = user_to_auth.password
    user = db.query(UserDB).filter_by(email=email).first()
    if not user:
        return False
    if not verify_password(plain_password, user.password):
        return False
    return user  # Sign In Function


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt  # Para crear el JWT
