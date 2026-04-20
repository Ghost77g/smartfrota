import secrets
import bcrypt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Usuario, PasswordResetToken


def get_user_by_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def generate_reset_token(db: Session, Usuario: Usuario) -> str:
    # Invalida tokens anteriores do mesmo usuário
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == Usuario.id,
        PasswordResetToken.used == False
    ).update({"used": True})

    # Gera token seguro de 64 caracteres hexadecimais
    token      = secrets.token_hex(32)
    expires_at = datetime.utcnow() + timedelta(minutes=30)

    reset_token = PasswordResetToken(
        user_id    = user.id,
        token      = token,
        expires_at = expires_at,
    )

    db.add(reset_token)
    db.commit()

    return token


def validate_reset_token(db: Session, token: str) -> PasswordResetToken | None:
    return db.query(PasswordResetToken).filter(
        PasswordResetToken.token      == token,
        PasswordResetToken.used       == False,
        PasswordResetToken.expires_at >  datetime.utcnow()
    ).first()


def update_password(db: Session, user_id, new_password: str):
    # Força da senha
    if len(new_password) < 8:
        raise ValueError("A senha deve ter no mínimo 8 caracteres.")

    hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt(rounds=12))

    user = db.query(User).filter(User.id == user_id).first()
    user.password = hashed.decode("utf-8")
    db.commit()


def invalidate_token(db: Session, reset_token: PasswordResetToken):
    reset_token.used = True
    db.commit()