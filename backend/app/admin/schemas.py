from pydantic import BaseModel
from typing import Optional


class AdminBase(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    password: Optional[str] = None

class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True
