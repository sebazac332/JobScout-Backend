from pydantic import BaseModel

class ExperienciaBase(BaseModel):
    cargo: str
    empresa: str
    duracao: str
    descricao: str | None = None

class ExperienciaCreate(ExperienciaBase):
    user_id: int

class Experiencia(ExperienciaBase):
    id: int

    class Config:
        orm_mode = True
