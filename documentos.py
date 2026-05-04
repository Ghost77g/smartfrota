import os
import uuid
import imghdr
import mimetypes
from pathlib import Path
from datetime import date
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from dependencies import pegar_sessao, verificar_token
from models import documento as Documento, Usuario

# ---------------------------------------------------------------------------
# Configurações de upload – centralizadas aqui para fácil auditoria
# ---------------------------------------------------------------------------

# Diretório onde os arquivos serão salvos.  Fora da raiz web, sem servir
# arquivos estáticos diretamente.
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads/documentos"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Limite máximo de tamanho: 10 MB
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

# Mapeamento: MIME type → extensão canônica que vamos usar no disco
ALLOWED_MIME_TYPES: dict[str, str] = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}

# Assinaturas mágicas (magic bytes) de cada tipo permitido.
# Tupla: (offset_inicial, bytes_esperados)
MAGIC_SIGNATURES: dict[str, list[tuple[int, bytes]]] = {
    "application/pdf": [(0, b"%PDF")],
    "image/jpeg":      [(0, b"\xff\xd8\xff")],
    "image/png":       [(0, b"\x89PNG\r\n\x1a\n")],
    "image/webp":      [(0, b"RIFF"), (8, b"WEBP")],
}

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

documento_router = APIRouter(prefix="/documentos", tags=["documentos"])


# ---------------------------------------------------------------------------
# Funções auxiliares de segurança
# ---------------------------------------------------------------------------

def _verificar_magic_bytes(header: bytes, mime_type: str) -> bool:
    """
    Verifica se os primeiros bytes do arquivo correspondem às assinaturas
    conhecidas para o MIME type declarado.  Previne execução de código
    disfarçado de PDF/imagem.
    """
    sigs = MAGIC_SIGNATURES.get(mime_type, [])
    for offset, expected in sigs:
        if header[offset: offset + len(expected)] != expected:
            return False
    return True


def _salvar_arquivo_com_segurança(upload: UploadFile) -> str:
    """
    Lê, valida e persiste o arquivo no disco.
    Retorna o nome gerado (UUID + extensão canônica).
    Lança HTTPException em caso de violação de segurança.
    """
    # 1. Verificar MIME type declarado pelo cliente
    content_type = (upload.content_type or "").split(";")[0].strip().lower()
    if content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                "Tipo de arquivo não permitido. "
                "Envie PDF, JPEG, PNG ou WebP."
            ),
        )

    # 2. Ler o arquivo inteiro de uma vez (permite verificar tamanho e magic bytes)
    contents = upload.file.read()

    # 3. Verificar tamanho
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Arquivo excede o limite de {MAX_FILE_SIZE_BYTES // (1024*1024)} MB.",
        )

    # 4. Verificar magic bytes – proteção contra RCE via arquivo malicioso
    if not _verificar_magic_bytes(contents, content_type):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "O conteúdo do arquivo não corresponde ao tipo declarado. "
                "Possível arquivo malicioso rejeitado."
            ),
        )

    # 5. Gerar nome aleatório – evita path traversal e sobrescrita
    ext = ALLOWED_MIME_TYPES[content_type]
    nome_seguro = f"{uuid.uuid4().hex}{ext}"
    destino = UPLOAD_DIR / nome_seguro

    # 6. Gravar com permissão restrita (somente dono pode ler/escrever)
    destino.write_bytes(contents)
    destino.chmod(0o640)

    return nome_seguro


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@documento_router.get(
    "/",
    summary="Listar documentos",
    description="Retorna todos os documentos cadastrados. Requer autenticação JWT.",
)
def listar_documentos(
    session: Session = Depends(pegar_sessao),
    _usuario: Usuario = Depends(verificar_token),
):
    """
    Lista todos os documentos em ordem de vencimento (mais próximos primeiro).
    Cada linha expõe: id, nome, tipo, data_emissao, data_vencimento.
    O campo `arquivo_nome` pode ser usado para construir a URL de download.
    """
    docs = (
        session.query(Documento)
        .order_by(Documento.data_vencimento.asc())
        .all()
    )

    return [
        {
            "id":              d.id,
            "nome":            d.nome,
            "tipo":            d.tipo,
            "data_emissao":    d.data_emissao.isoformat() if d.data_emissao else None,
            "data_vencimento": d.data_vencimento.isoformat() if d.data_vencimento else None,
            "arquivo_nome":    d.arquivo_nome,
            "veiculo_id":      d.veiculo_id,
        }
        for d in docs
    ]


@documento_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar documento",
    description=(
        "Cadastra um documento com upload de arquivo (PDF, JPEG, PNG ou WebP). "
        "O arquivo é validado por tipo, tamanho e assinatura mágica antes de ser salvo. "
        "Requer autenticação JWT."
    ),
)
async def criar_documento(
    nome:            str  = Form(..., min_length=1, max_length=255),
    tipo:            str  = Form(..., min_length=1, max_length=100),
    data_emissao:    date = Form(...),
    data_vencimento: date = Form(...),
    veiculo_id:      Optional[int] = Form(None),
    arquivo:         UploadFile = File(...),
    session:         Session = Depends(pegar_sessao),
    _usuario:        Usuario = Depends(verificar_token),
):
    """
    Recebe os metadados via Form e o arquivo via multipart.
    Valida datas, salva o arquivo com nome gerado por UUID e persiste os
    metadados no banco de dados.
    """

    # Validação de negócio: vencimento não pode ser anterior à emissão
    if data_vencimento < data_emissao:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A data de vencimento não pode ser anterior à data de emissão.",
        )

    # Salvar arquivo com verificações de segurança
    arquivo_nome = _salvar_arquivo_com_segurança(arquivo)

    # Persistir no banco
    novo_doc = Documento(
        nome=nome,
        tipo=tipo,
        data_emissao=data_emissao,
        data_vencimento=data_vencimento,
        arquivo_nome=arquivo_nome,
        veiculo_id=veiculo_id,
    )
    session.add(novo_doc)
    session.commit()
    session.refresh(novo_doc)

    return {
        "id":              novo_doc.id,
        "nome":            novo_doc.nome,
        "tipo":            novo_doc.tipo,
        "data_emissao":    novo_doc.data_emissao.isoformat(),
        "data_vencimento": novo_doc.data_vencimento.isoformat(),
        "arquivo_nome":    novo_doc.arquivo_nome,
        "veiculo_id":      novo_doc.veiculo_id,
        "mensagem":        "Documento cadastrado com sucesso.",
    }


@documento_router.get(
    "/{documento_id}/download",
    summary="Download de arquivo do documento",
    description="Faz download do arquivo associado a um documento. Requer autenticação JWT.",
)
def download_documento(
    documento_id: int,
    session:      Session = Depends(pegar_sessao),
    _usuario:     Usuario = Depends(verificar_token),
):
    """
    Serve o arquivo do documento de forma segura.
    - Garante que o arquivo existe no banco e no disco.
    - Nunca expõe o caminho real no sistema de arquivos.
    - Usa Content-Disposition: attachment para forçar download.
    """
    doc = session.query(Documento).filter(Documento.id == documento_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento não encontrado.")

    if not doc.arquivo_nome:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Este documento não possui arquivo associado.")

    # Montar caminho absoluto e verificar que está dentro do UPLOAD_DIR
    caminho = (UPLOAD_DIR / doc.arquivo_nome).resolve()
    try:
        caminho.relative_to(UPLOAD_DIR.resolve())
    except ValueError:
        # Path traversal detectado
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")

    if not caminho.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo não encontrado no servidor.")

    # Determinar MIME type pelo nome seguro (extensão canônica)
    media_type, _ = mimetypes.guess_type(str(caminho))
    media_type = media_type or "application/octet-stream"

    # Nome amigável para o download: nome do documento + extensão
    ext = caminho.suffix
    nome_download = f"{doc.nome}{ext}".replace(" ", "_")

    return FileResponse(
        path=str(caminho),
        media_type=media_type,
        filename=nome_download,
    )


@documento_router.delete(
    "/{documento_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir documento",
    description="Remove o documento e seu arquivo do sistema. Requer autenticação JWT.",
)
def excluir_documento(
    documento_id: int,
    session:      Session = Depends(pegar_sessao),
    _usuario:     Usuario = Depends(verificar_token),
):
    doc = session.query(Documento).filter(Documento.id == documento_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento não encontrado.")

    # Remover arquivo do disco, se existir
    if doc.arquivo_nome:
        caminho = (UPLOAD_DIR / doc.arquivo_nome).resolve()
        try:
            caminho.relative_to(UPLOAD_DIR.resolve())
            if caminho.is_file():
                caminho.unlink()
        except ValueError:
            pass  # path traversal – ignora silenciosamente, só deleta do banco

    session.delete(doc)
    session.commit()
    # 204 No Content – sem corpo na resposta