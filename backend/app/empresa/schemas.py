from pydantic import BaseModel
from typing import Optional

class EmpresaBase(BaseModel):
    nome: str
    descricao: str
    cidade: str
    cep: str
    no_empregados: int
    anos_func: int

class EmpresaCreate(EmpresaBase):
    admin_id: int

class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[str] = None
    no_empregados: Optional[int] = None
    anos_func: Optional[int] = None

class Empresa(EmpresaBase):
    id: int

    class Config:
        orm_mode = True