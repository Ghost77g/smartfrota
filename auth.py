from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACESS_TOKEN_EXPIRE, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(usuario, duracao_token = timedelta(days=ACESS_TOKEN_EXPIRE)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(usuario.id), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY)
    return jwt_codificado

def verificar_token(token, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id==1).first
    return usuario


def autenticar_conta(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise(HTTPException(status_code=400, detail="usuario ou senha incorreto"))
    elif not bcrypt_context.verify(senha, usuario.senha):
        raise(HTTPException(status_code=400, detail="usuario ou senha incorreto"))
    return usuario


@auth_router.get("/")
async def auth():
    return {"mensagem" "voce acessou a rota de autenticacão"}
