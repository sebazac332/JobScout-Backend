from sqlalchemy.orm import Session

from app.model import models
from . import schemas
from fastapi import HTTPException

def create_vagaemprego(db: Session, vaga: schemas.VagaCreate):
    db_vaga = models.Vagaemprego(**vaga.model_dump())
    db.add(db_vaga)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga

def get_vagas_by_empresa(db: Session, empresa_id: int):
    return db.query(models.Vagaemprego).filter(models.Vagaemprego.empresa_id == empresa_id).all()

def add_competencia_to_vaga(db: Session, vaga_id: int, competencia_id: int):
    vaga = db.query(models.Vagaemprego).get(vaga_id)
    competencia = db.query(models.Competencia).get(competencia_id)

    if not vaga or not competencia:
        raise HTTPException(status_code=404, detail="Vaga ou competência não encontrada")

    if competencia in vaga.competencias:
        raise HTTPException(status_code=400, detail="Competência já associada à vaga")

    vaga.competencias.append(competencia)
    db.commit()
    return {"message": "Competência adicionada à vaga com sucesso"}


def remove_competencia_from_vaga(db: Session, vaga_id: int, competencia_id: int):
    vaga = db.query(models.Vagaemprego).get(vaga_id)
    competencia = db.query(models.Competencia).get(competencia_id)

    if not vaga or not competencia:
        raise HTTPException(status_code=404, detail="Vaga ou competência não encontrada")

    if competencia not in vaga.competencias:
        raise HTTPException(status_code=400, detail="Competência não associada à vaga")

    vaga.competencias.remove(competencia)
    db.commit()
    return {"message": "Competência removida da vaga com sucesso"}

def get_vaga_competencias(db: Session, vaga_id: int):
    vaga = db.query(models.Vagaemprego).filter(models.Vagaemprego.id == vaga_id).first()
    if not vaga:
        return {"error": "Vaga not found"}
    return vaga.competencias