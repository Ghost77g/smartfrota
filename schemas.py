from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date


class UsuarioSchema(BaseModel):
    name: str
    senha: str
    email: str
    telefone: str
    ativo: Optional[bool] = None
    admin: Optional[bool] = None

    class Config:
        from_attributes = True


class veiculoSchema(BaseModel):
    modelo: str
    marca: str
    placa: str

    class Config:
        from_attributes = True


# ── Documentos ───────────────────────────────────────────────────────────────

class DocumentoResponse(BaseModel):
    """Schema de saída (leitura) de um documento."""
    id: int
    nome: str
    tipo: str
    data_emissao: date
    data_vencimento: date
    arquivo_nome: Optional[str] = None
    veiculo_id: Optional[int] = None

    class Config:
        from_attributes = True


# Nota: DocumentoCreate não é necessário aqui porque o endpoint usa Form() +
# UploadFile diretamente (multipart/form-data).  O schema de validação ocorre
# no próprio roteador via parâmetros Form e FastAPI.

# ── Auth ─────────────────────────────────────────────────────────────────────

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    class Config:
        from_attributes = True


# ── Motoristas ────────────────────────────────────────────────────────────────

class MotoristaSchema(BaseModel):
    nome_usuario: str
    cnh: str

    class Config:
        from_attributes = True


class MotoristaResponse(BaseModel):
    id: int
    usuario_id: int
    cnh: str

    class Config:
        from_attributes = True