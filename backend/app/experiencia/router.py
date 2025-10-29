from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions

router = APIRouter(prefix="/experiencias", tags=["Experiencias"])

@router.post("/", response_model=schemas.Experiencia)
def create_experiencia(exp: schemas.ExperienciaCreate, db: Session = Depends(get_db)):
    return functions.create_experiencia(db, exp)

@router.get("/experiencias/user/{user_id}", response_model=list[schemas.Experiencia])
def list_experiencias(user_id: int, db: Session = Depends(get_db)):
    experiencias = functions.get_experiencias_by_user(db, user_id)
    if not experiencias:
        raise HTTPException(status_code=404, detail="No experiences found for this user")
    return experiencias