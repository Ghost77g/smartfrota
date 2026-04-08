from sqlalchemy import ForeignKey, create_engine, Column, String, Integer, Float, Boolean, Date, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy import ForeignKey, create_engine, Column, String, Integer, Float, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType
from database import Base
import enum

db = create_engine("postgresql://postgres:gm080507@localhost:5432/smartfrota.db")
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"  # padronizado minúsculo

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    função = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    def __init__(self, nome, senha, email, telefone, função , ativo=True, admin=False):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.telefone = telefone
        self.função = função
        self.ativo = ativo
        self.admin = admin


class StatusVeiculo(enum.Enum):
    PRONTO = "Pronto para uso"
    EM_USO = "Em uso"
    QUEBRADO = "Quebrado"
    IRREGULAR = "Irregular"
    MANUTENCAO = "Em manutenção"


class Veiculo(Base):
    __tablename__ = "veiculos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    modelo = Column(String, nullable=False)
    marca = Column(String, nullable=False)
    placa = Column(String, nullable=False)
    preco = Column(Float, nullable=True)
    motorista_id = Column()

    status = Column(
        Enum(StatusVeiculo, name="status_veiculo_enum"),
        default=StatusVeiculo.PRONTO,
        nullable=False
    )

    def __init__(self, modelo, marca, placa, preco=0, status=StatusVeiculo.PRONTO):
        self.modelo = modelo
        self.marca = marca
        self.placa = placa
        self.preco = preco
        self.status = status

class manutenção(Base):
    __tablename__ = "manutenções"

    id = Column(Integer, primary_key=True, autoincrement=True)  # corrigido
    valor = Column(Float)
    tipo = Column(String, nullable=False)
    oficina_responsavel = Column(String, nullable=False)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"))  # corrigido

    def __init__(self, valor, tipo, oficina_responsavel):
        self.valor = valor
        self.tipo = tipo
        self.oficina_responsavel = oficina_responsavel

class documento(Base):
    __tablename__ = "Documentos"

    id = Column(Integer, primary_key=True, autoincrement=True)  # corrigido
    tipo = Column(String, nullable=False)
    data_emissao = Column(Date, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"))  # corrigido

    def __init__(self, tipo, data_emissao, data_vencimento):
        self.tipo = tipo
        self.data_emissao = data_emissao
        self.data_vencimento = data_vencimento

class motorista_veiculo(Base):
    __tablename__ = "Motorista-veiculo"

    id = Column(Integer, primary_key=True, autoincrement=True)  # corrigido
    veiculo_id = Column(Integer, ForeignKey("veiculos.id")) 
    motorista_id = Column(Integer, ForeignKey("usuarios.id"))  # corrigido
    data_inicio = Column(Date)
    data_fim = Column(Date)

    def __init__(self, veiculo_id, motorist_id, data_inicio, data_fim):
        self.veiculo_id = veiculo_id
        self. motorist_id = motorist_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim