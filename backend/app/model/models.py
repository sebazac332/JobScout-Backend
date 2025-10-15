from sqlalchemy import Column, Integer, String
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=False, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, unique=False, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

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