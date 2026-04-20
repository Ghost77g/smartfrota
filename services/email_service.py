from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração do servidor SMTP
conf = ConnectionConfig(
    MAIL_USERNAME   = os.getenv("SMTP_USER"),
    MAIL_PASSWORD   = os.getenv("SMTP_PASS"),
    MAIL_FROM       = os.getenv("SMTP_FROM"),
    MAIL_PORT       = 587,
    MAIL_SERVER     = os.getenv("SMTP_HOST"),
    MAIL_STARTTLS   = True,
    MAIL_SSL_TLS    = False,
)

async def send_reset_email(to: str, name: str, reset_link: str):
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
        <h2 style="color: #1d4ed8;"> Sistema de Gestão de Frotas</h2>
        <p>Olá, <strong>{name}</strong>!</p>
        <p>Recebemos uma solicitação para redefinir sua senha.</p>
        <p>Clique no botão abaixo para criar uma nova senha:</p>

        <a href="{reset_link}" style="
            display: inline-block;
            background: #1d4ed8;
            color: #fff;
            padding: 12px 28px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            margin: 16px 0;
        ">
            Redefinir Senha
        </a>

        <p> Este link expira em <strong>30 minutos</strong>.</p>
        <p style="color: #6b7280;">Se não foi você, ignore este e-mail com segurança.</p>
    </div>
    """

    message = MessageSchema(
        subject    = "Recuperação de Senha — Gestão de Frotas",
        recipients = [to],
        body       = html_body,
        subtype    = "html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)