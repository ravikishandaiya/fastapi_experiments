from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash(password:str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)