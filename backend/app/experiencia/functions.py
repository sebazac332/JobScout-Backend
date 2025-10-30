from sqlalchemy.orm import Session

from app.model import models
from . import schemas

def create_experiencia(db: Session, exp: schemas.ExperienciaCreate):
    db_exp = models.Experiencia(**exp.model_dump())
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

def update_experiencia(db: Session, experiencia_id: int, experiencia_update: schemas.ExperienciaUpdate):
    db_experiencia = db.query(models.Experiencia).filter(models.Experiencia.id == experiencia_id).first()

    if not db_experiencia:
        return None

    if experiencia_update.cargo is not None:
        db_experiencia.cargo = db_experiencia.cargo
    if experiencia_update.empresa is not None:
        db_experiencia.empresa = db_experiencia.empresa
    if experiencia_update.anos is not None:
        db_experiencia.anos = db_experiencia.anos

    db.commit()
    db.refresh(db_experiencia)
    return db_experiencia

def delete_experiencia(db: Session, experiencia_id: int):
    db_experiencia = db.query(models.Experiencia).filter(models.Experiencia.id == experiencia_id).first()

    if not db_experiencia:
        return None

    db.delete(db_experiencia)
    db.commit()
    return db_experiencia

def get_experiencias_by_user(db: Session, user_id: int):
    return db.query(models.Experiencia).filter(models.Experiencia.user_id == user_id).all()