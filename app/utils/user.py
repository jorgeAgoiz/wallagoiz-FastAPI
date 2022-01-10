from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from pydantic.main import BaseModel
from sqlalchemy.orm.session import Session
from starlette import status
from utils.hash_password import verify_password
from utils.hash_password import get_password_hash
from models.user import UserSignIn
from models.user import CreateUser
from models.user import UserDB
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


load_dotenv()  # Variables de entorno para JWT
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


class TokenData(BaseModel):
    id: Optional[int] = None

# User Functions


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_all_users(db: Session, skip: int, limit: int):
    return db.query(UserDB).all()
    # Funcion dame todos los usuarios


def get_user_by_id(db: Session, id: int):
    return db.query(UserDB).filter_by(id=id).first()
    # Funcion dame un usuario específico por ID


def create_new_user(user: CreateUser, db: Session):
    user.password = get_password_hash(user.password)
    new_user = UserDB(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user  # Sign Up Function


def authenticate_user(user_to_auth: UserSignIn, db: Session):
    email = user_to_auth.email
    plain_password = user_to_auth.password
    user: CreateUser = db.query(UserDB).filter_by(
        email=email).first()  # Buscamos por email al usuario
    if not user:
        return False
    if not verify_password(plain_password, user.password):
        return False
    return user  # Devolvemos un usuario completo de la BBDD al SignIn


def verify_access_token(token: str, credentials_exception):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    id: int = payload.get("user_id")
    print(id)

# def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("user_email")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(email=email)
#     except JWTError:
#         raise credentials_exception
#     user = db.query(UserDB).filter_by(email=token_data.email).first()
#     if user is None:
#         raise credentials_exception
#     return token_data
