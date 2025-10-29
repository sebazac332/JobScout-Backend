from pydantic import BaseModel
from app.competencia.schemas import Competencia

class VagasBase(BaseModel):
    titulo: str
    descricao: str
    modalidade: str
    salario: float
    no_vagas: int

class VagaCreate(VagasBase):
    empresa_id: int

class Vaga(VagasBase):
    id: int
    empresa_id: int
    competencias: list[Competencia] = []

    class Config:
        orm_mode = True