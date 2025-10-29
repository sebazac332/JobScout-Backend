from sqlalchemy.orm import Session

from app.model import models
from . import schemas

def create_experiencia(db: Session, exp: schemas.ExperienciaCreate):
    db_exp = models.Experiencia(**exp.model_dump())
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

def get_experiencias_by_user(db: Session, user_id: int):
    return db.query(models.Experiencia).filter(models.Experiencia.user_id == user_id).all()