# config.py
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE = int(os.getenv("ACESS_TOKEN_EXPIRE"))

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAuth2schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")