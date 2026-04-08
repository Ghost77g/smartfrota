from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
from config import bcrypt_context, ALGORITHM, ACESS_TOKEN_EXPIRE, SECRET_KEY

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(usuario, duracao_token = timedelta(days=ACESS_TOKEN_EXPIRE)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(usuario.id), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

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

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema:UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="email ja cadastrado")
    else:
        senha_cript = bcrypt_context.hash(usuario_schema.senha)
        new_user = Usuario(usuario_schema.name, senha_cript,usuario_schema.email,usuario_schema.telefone, usuario_schema.ativo, usuario_schema.admin)
        session.add(new_user)
        session.commit()
        return("mensagem" "usuario cadastrado")

@auth_router.post("/login-form")
async def login_form( data_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_conta(data_form.username, data_form.password, session)
    if not usuario:
        raise(HTTPException(status_code=400, detail="usuario não encontrado"))
    else:
        acess_token = criar_token(usuario)
        refresh_token = criar_token(usuario, duracao_token = timedelta(days=7))
        return{
            "access_token": acess_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

@auth_router.post("/login")
async def login( login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_conta(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise(HTTPException(status_code=400, detail="usuario não encontrado"))
    else:
        acess_token = criar_token(usuario)
        refresh_token = criar_token(usuario, duracao_token = timedelta(days=7))
        return{
            "access_token": acess_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    acess_token = criar_token(usuario)
    return{
        "access_token": acess_token,
        "token_type": "bearer"
    }
