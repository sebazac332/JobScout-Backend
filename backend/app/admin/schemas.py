from pydantic import BaseModel

class AdminBase(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str

class AdminCreate(AdminBase):
    password: str

class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True
