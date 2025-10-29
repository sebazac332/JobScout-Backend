from pydantic import BaseModel

class EmpresaBase(BaseModel):
    nome: str
    descricao: str
    cidade: str
    cep: str
    no_empregados: int
    anos_func: int

class EmpresaCreate(EmpresaBase):
    admin_id: int

class Empresa(EmpresaBase):
    id: int

    class Config:
        orm_mode = True