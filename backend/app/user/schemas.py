from pydantic import BaseModel

class UserBase(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str
    area_trabalho: str
    nivel_educacao: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
