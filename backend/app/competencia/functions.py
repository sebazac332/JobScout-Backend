from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.model import models
from . import schemas

def create_competencia(db: Session, competencia: schemas.CompetenciaCreate):
    existing = db.query(models.Competencia).filter(models.Competencia.nome == competencia.nome).first()
    if existing:
        raise HTTPException(status_code=400, detail="Competência já existe")

    db_competencia = models.Competencia(nome=competencia.nome)
    db.add(db_competencia)
    db.commit()
    db.refresh(db_competencia)
    return db_competencia


def get_competencias(db: Session):
    return db.query(models.Competencia).all()