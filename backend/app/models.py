from sqlalchemy import Column, Integer, String
from .database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=False, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, unique=False, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
