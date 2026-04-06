from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from database import engine, Base

app = FastAPI()

bcrypt_context = CryptContext(schemes =["bcrypt"], deprecated="auto")
OAuth2schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routers import auth_router

app.include_router(auth_router)