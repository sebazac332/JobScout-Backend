from pydantic import BaseModel
from app.competencia.schemas import Competencia
from typing import Optional

class UserBase(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str
    area_trabalho: str
    nivel_educacao: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    password: Optional[str] = None
    area_trabalho: Optional[str] = None
    nivel_educacao: Optional[str] = None

class User(UserBase):
    id: int
    competencias: list[Competencia] = []

    class Config:
        orm_mode = True
