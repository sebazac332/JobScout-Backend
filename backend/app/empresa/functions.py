from sqlalchemy.orm import Session

from app.model import models
from . import schemas

def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    db_empresa = models.Empresa(
        nome=empresa.nome,
        descricao=empresa.descricao,
        cidade=empresa.cidade,
        cep=empresa.cep,
        no_empregados=empresa.no_empregados,
        anos_func=empresa.anos_func,
        admin_id=empresa.admin_id
    )
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

def get_empresas(db: Session):
    return db.query(models.Empresa).all()

def get_empresas_by_admin(db: Session, admin_id: int):
    return db.query(models.Empresa).filter(models.Empresa.admin_id == admin_id).all()