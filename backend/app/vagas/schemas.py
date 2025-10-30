from pydantic import BaseModel
from app.competencia.schemas import Competencia
from typing import Optional

class VagasBase(BaseModel):
    titulo: str
    descricao: str
    modalidade: str
    salario: float
    no_vagas: int

class VagaCreate(VagasBase):
    empresa_id: int

class VagaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    modalidade: Optional[str] = None
    salario: Optional[str] = None
    no_vagas: Optional[int] = None

class Vaga(VagasBase):
    id: int
    empresa_id: int
    competencias: list[Competencia] = []

    class Config:
        orm_mode = True