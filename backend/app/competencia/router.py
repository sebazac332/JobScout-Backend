from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions

router = APIRouter(prefix="/competencias", tags=["Competencias"])

@router.post("/", response_model=schemas.Competencia)
def create_competencia(competencia: schemas.CompetenciaCreate, db: Session = Depends(get_db)):
    return functions.create_competencia(db, competencia)

@router.get("/", response_model=list[schemas.Competencia])
def list_competencias(db: Session = Depends(get_db)):
    return functions.get_competencias(db)