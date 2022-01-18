from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from models.token import TokenData, oauth2_scheme
from utils.hash_password import verify_password
from utils.hash_password import get_password_hash
from models.user import UserSignIn
from models.user import CreateUser
from models.user import UserDB
from jose import JWTError, jwt
import os
from dotenv import load_dotenv


load_dotenv()  # Variables de entorno para JWT
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def get_all_users(db: Session):
    return db.query(UserDB).all()


def get_user_by_id(db: Session, id: int):
    return db.query(UserDB).filter_by(id=id).first()


def create_new_user(user: CreateUser, db: Session):
    user.password = get_password_hash(user.password)
    new_user = UserDB(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(user_to_auth: UserSignIn, db: Session):
    email = user_to_auth.email
    plain_password = user_to_auth.password
    user: CreateUser = db.query(UserDB).filter_by(
        email=email).first()
    if not user:
        return False
    if not verify_password(plain_password, user.password):
        return False
    return user


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError as err:
        raise credentials_exception

    return token_data.id


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)


def delete_user(user_id: str, db: Session):
    user = db.query(UserDB).filter_by(
        id=user_id).delete(synchronize_session=False)
    if user == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="User not found.")
    db.commit()
    return user
