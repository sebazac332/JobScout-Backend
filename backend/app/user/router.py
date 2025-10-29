from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if functions.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if functions.get_user_by_cpf(db, user.cpf):
        raise HTTPException(status_code=400, detail="CPF already registered")
    return functions.create_user(db, user)

@router.post("/{user_id}/competencias/{competencia_id}")
def add_competencia(user_id: int, competencia_id: int, db: Session = Depends(get_db)):
    return functions.add_competencia_to_user(db, user_id, competencia_id)

@router.delete("/{user_id}/competencias/{competencia_id}")
def remove_competencia(user_id: int, competencia_id: int, db: Session = Depends(get_db)):
    return functions.remove_competencia_from_user(db, user_id, competencia_id)

@router.get("/{user_id}/competencias")
def list_competencias(user_id: int, db: Session = Depends(get_db)):
    return functions.get_user_competencias(db, user_id)