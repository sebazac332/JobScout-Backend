from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions

router = APIRouter(prefix="/competencias", tags=["Competencias"])

@router.post("/", response_model=schemas.Competencia)
def create_competencia(competencia: schemas.CompetenciaCreate, db: Session = Depends(get_db)):
    return functions.create_competencia(db, competencia)

@router.delete("/{competencia_id}", response_model=schemas.Competencia)
def delete_competencia(competencia_id: int, db: Session = Depends(get_db)):
    deleted_competencia = functions.delete_competencia(db, competencia_id)
    if not deleted_competencia:
        raise HTTPException(status_code=404, detail="Competência não encontrada")
    return deleted_competencia

@router.get("/", response_model=list[schemas.Competencia])
def list_competencias(db: Session = Depends(get_db)):
    return functions.get_competencias(db)