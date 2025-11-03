from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions
from app.dependencies.auth import get_current_regular_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if functions.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email já registrado")
    if functions.get_user_by_cpf(db, user.cpf):
        raise HTTPException(status_code=400, detail="CPF já registrado")
    return functions.create_user(db, user)

@router.put("/{user_id}", response_model=schemas.User)
def edit_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = functions.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    return user

@router.delete("/{user_id}", response_model=schemas.User)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = functions.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    return user

@router.post("/{user_id}/competencias/{competencia_id}")
def add_competencia(user_id: int, competencia_id: int, db: Session = Depends(get_db)):
    added = functions.add_competencia_to_user(db, user_id, competencia_id)
    return added

@router.delete("/{user_id}/competencias/{competencia_id}")
def remove_competencia(user_id: int, competencia_id: int, db: Session = Depends(get_db)):
    deleted = functions.remove_competencia_from_user(db, user_id, competencia_id)
    return deleted

@router.get("/{user_id}/competencias")
def list_competencias(user_id: int, db: Session = Depends(get_db)):
    list = functions.get_user_competencias(db, user_id)
    return list