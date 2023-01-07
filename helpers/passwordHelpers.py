from passlib.context import CryptContext


#   Decode password from weird str
def verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


#   Encode password int weird str
def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)