from fastapi import APIRouter, Depends, HTTPException
from main import bcrypt_context
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    return {"mensagem" "voce acessou a rota de autenticacão"}