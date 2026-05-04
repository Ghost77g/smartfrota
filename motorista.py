import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_gestor
from models import Usuario, Motorista
from schemas import MotoristaSchema, MotoristaResponse

motorista_router = APIRouter(prefix="/motoristas", tags=["motoristas"])


def _validar_cnh(cnh: str) -> bool:
    """
    Valida o formato básico da CNH brasileira:
    - 11 dígitos numéricos
    - Não pode ser sequência repetida (ex: 11111111111)
    """
    if not re.fullmatch(r"\d{11}", cnh):
        return False
    if len(set(cnh)) == 1:
        return False
    return True


@motorista_router.post(
    "/cadastrar",
    response_model=MotoristaResponse,
    summary="Cadastrar motorista",
    description="Rota restrita a gestores (admin=True). Recebe o nome de um usuário já cadastrado e uma CNH válida.",
)
async def cadastrar_motorista(
    dados: MotoristaSchema,
    session: Session = Depends(pegar_sessao),
    _gestor: Usuario = Depends(verificar_gestor),
):
    # 1. Verificar se o usuário existe pelo nome
    usuario = session.query(Usuario).filter(Usuario.nome == dados.nome_usuario).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário '{dados.nome_usuario}' não encontrado.",
        )

    # 2. Verificar se o usuário já é motorista cadastrado
    ja_cadastrado = (
        session.query(Motorista).filter(Motorista.usuario_id == usuario.id).first()
    )
    if ja_cadastrado:
        raise HTTPException(
            status_code=409,
            detail="Este usuário já possui um cadastro de motorista.",
        )

    # 3. Validar formato da CNH
    if not _validar_cnh(dados.cnh):
        raise HTTPException(
            status_code=422,
            detail="CNH inválida. Deve conter exatamente 11 dígitos numéricos e não pode ser uma sequência repetida.",
        )

    # 4. Verificar se a CNH já está em uso
    cnh_existente = (
        session.query(Motorista).filter(Motorista.cnh == dados.cnh).first()
    )
    if cnh_existente:
        raise HTTPException(
            status_code=409,
            detail="Esta CNH já está cadastrada no sistema.",
        )

    # 5. Inserir motorista no banco
    novo_motorista = Motorista(usuario_id=usuario.id, cnh=dados.cnh)
    session.add(novo_motorista)
    session.commit()
    session.refresh(novo_motorista)

    return novo_motorista