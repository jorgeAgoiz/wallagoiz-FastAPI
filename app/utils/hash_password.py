from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)
    # Función para hashear el password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    # Esta función para el sign in, verificación de password
