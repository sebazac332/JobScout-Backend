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

def update_empresa(db: Session, empresa_id: int, empresa_update: schemas.EmpresaUpdate):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()

    if not db_empresa:
        return None

    if empresa_update.nome is not None:
        db_empresa.nome = empresa_update.nome
    if empresa_update.descricao is not None:
        db_empresa.descricao = empresa_update.descricao
    if empresa_update.cidade is not None:
        db_empresa.cidade = empresa_update.cidade
    if empresa_update.cep is not None:
        db_empresa.cep = empresa_update.cep
    if empresa_update.no_empregados is not None:
        db_empresa.no_empregados = empresa_update.no_empregados
    if empresa_update.anos_func is not None:
        db_empresa.anos_func = empresa_update.anos_func

    db.commit()
    db.refresh(db_empresa)
    return db_empresa

def delete_empresa(db: Session, empresa_id: int):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()

    if not db_empresa:
        return None

    db.delete(db_empresa)
    db.commit()
    return db_empresa

def get_empresas(db: Session):
    return db.query(models.Empresa).all()

def get_empresas_by_admin(db: Session, admin_id: int):
    return db.query(models.Empresa).filter(models.Empresa.admin_id == admin_id).all()