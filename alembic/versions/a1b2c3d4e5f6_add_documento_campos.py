"""add nome and arquivo_nome to Documentos table

Revision ID: a1b2c3d4e5f6
Revises: f46e07dff2dd
Create Date: 2026-05-03 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "f46e07dff2dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adiciona coluna 'nome' (obrigatória) com valor temporário para linhas existentes
    op.add_column(
        "Documentos",
        sa.Column("nome", sa.String(255), nullable=True),
    )
    # Preenche linhas existentes com valor padrão antes de tornar NOT NULL
    op.execute("UPDATE \"Documentos\" SET nome = tipo WHERE nome IS NULL")
    op.alter_column("Documentos", "nome", nullable=False)

    # Adiciona coluna 'arquivo_nome' (opcional)
    op.add_column(
        "Documentos",
        sa.Column("arquivo_nome", sa.String(255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("Documentos", "arquivo_nome")
    op.drop_column("Documentos", "nome")
