from pydantic import BaseModel

class CompetenciaBase(BaseModel):
    nome: str

class CompetenciaCreate(CompetenciaBase):
    pass

class Competencia(CompetenciaBase):
    id: int

    class Config:
        from_attributes = True