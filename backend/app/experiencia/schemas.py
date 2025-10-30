from pydantic import BaseModel
from typing import Optional

class ExperienciaBase(BaseModel):
    cargo: str
    empresa: str
    anos: int

class ExperienciaCreate(ExperienciaBase):
    user_id: int

class ExperienciaUpdate(BaseModel):
    cargo: Optional[str] = None
    empresa: Optional[str] = None
    anos: Optional[int] = None

class Experiencia(ExperienciaBase):
    id: int

    class Config:
        orm_mode = True
