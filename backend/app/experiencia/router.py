from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions

router = APIRouter(prefix="/experiencias", tags=["Experiencias"])

@router.post("/", response_model=schemas.Experiencia)
def create_experiencia(exp: schemas.ExperienciaCreate, db: Session = Depends(get_db)):
    return functions.create_experiencia(db, exp)

@router.put("/experiencias/{experiencia_id}", response_model=schemas.Empresa)
def update_experiencia(experiencia_id: int, experiencia_update: schemas.ExperienciaUpdate, db: Session = Depends(get_db)):
    updated = functions.update_empresa(db, experiencia_id, experiencia_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Experiencia não encontrada")
    return updated

@router.delete("/experiencias/{experiencia_id}", response_model=schemas.Empresa)
def delete_empresa(experiencia_id: int, db: Session = Depends(get_db)):
    deleted = functions.delete_empresa(db, experiencia_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Experiencia não encontrada")
    return deleted

@router.get("/experiencias/user/{user_id}", response_model=list[schemas.Experiencia])
def list_experiencias(user_id: int, db: Session = Depends(get_db)):
    experiencias = functions.get_experiencias_by_user(db, user_id)
    if not experiencias:
        raise HTTPException(status_code=404, detail="No experiences found for this user")
    return experiencias