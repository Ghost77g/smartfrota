from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from database import engine, Base

app = FastAPI()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE = int(os.getenv("ACESS_TOKEN_EXPIRE"))


bcrypt_context = CryptContext(schemes =["bcrypt"], deprecated="auto")
OAuth2schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routers import auth_router

app.include_router(auth_router)