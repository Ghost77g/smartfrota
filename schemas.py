from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UsuarioSchema(BaseModel):
    name:str
    senha:str
    email:str
    telefone:str
    ativo:Optional[bool]
    admin:Optional[bool]

    class config:
        from_attributes = True
    
class veiculoSchema(BaseModel):
        modelo:str
        marca:str
        placa:str

        class config:
            from_attributes = True

class DocumentoSchema(BaseModel):
    tipo:str
    data_inicio:date
    data_fim:date

class LoginSchema(BaseModel):
    email:str
    senha:str

    class config:
        from_attributes = True

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    class config:
        from_attributes = True

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    class config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str

    class config:
        from_attributes = True