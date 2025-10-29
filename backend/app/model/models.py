from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=False, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, unique=False, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    empresas = relationship("Empresa", back_populates="admin")

user_competencia = Table(
    "user_competencia",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("competencia_id", Integer, ForeignKey("competencias.id")),
)

vaga_competencia = Table(
    "vaga_competencia",
    Base.metadata,
    Column("vaga_id", Integer, ForeignKey("vaga_emprego.id")),
    Column("competencia_id", Integer, ForeignKey("competencias.id")),
)

class Competencia(Base):
    __tablename__ = "competencias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)

    usuarios = relationship("User", secondary=user_competencia, back_populates="competencias")
    vagas = relationship("Vagaemprego", secondary=vaga_competencia, back_populates="competencias")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=False, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, unique=False, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    area_trabalho = Column(String, unique=False, index=True, nullable=False)
    nivel_educacao = Column(String, unique=False, index=True, nullable=False)

    vagas_aplicadas = relationship(
        "Vagaemprego",
        secondary="user_vaga_association",
        back_populates="candidatos",
    )

    experiencias = relationship("Experiencia", back_populates="user", cascade="all, delete")

    competencias = relationship("Competencia", secondary=user_competencia, back_populates="usuarios")

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=False, index=True, nullable=False)
    descricao = Column(String, unique=False, index=True, nullable=False)
    cidade = Column(String, unique=False, index=True, nullable=False)
    cep = Column(String, unique=False, index=True, nullable=False)
    no_empregados = Column(Integer, unique=False, index=True, nullable=False)
    anos_func = Column(Integer, unique=False, index=True, nullable=False)
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)

    admin = relationship("Admin", back_populates="empresas")

    vagas = relationship("Vagaemprego", back_populates="empresa")

class Vagaemprego(Base):
    __tablename__ = "vaga_emprego"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, unique=False, index=True, nullable=False)
    descricao = Column(String, unique=False, index=True, nullable=False)
    modalidade = Column(String, unique=False, index=True, nullable=False)
    salario = Column(Float, unique=False, index=True, nullable=False)
    no_vagas = Column(Integer, unique=False, index=True, nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("Empresa", back_populates="vagas")

    candidatos = relationship(
        "User",
        secondary="user_vaga_association",
        back_populates="vagas_aplicadas",
    )

    competencias = relationship("Competencia", secondary=vaga_competencia, back_populates="vagas")

user_vaga_association = Table(
    "user_vaga_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("vaga_id", Integer, ForeignKey("vaga_emprego.id"), primary_key=True),
)

class Experiencia(Base):
    __tablename__ = "experiencias"

    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(String, unique=False, index=True, nullable=False)
    cargo = Column(String, unique=False, index=True, nullable=False)
    anos = Column(Integer, unique=False, index=True, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="experiencias")