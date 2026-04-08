from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, OAuth2schema

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(OAuth2schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, details="acesso negado, verifique a validadade do token")

    usuario = session.query(Usuario).filter(Usuario.id==1).first
    if not usuario:
        raise HTTPException(status_code=401, details="acesso negado")

    return usuario