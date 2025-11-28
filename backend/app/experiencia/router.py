from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions
from app.dependencies.auth import get_current_regular_user, get_current_user

router = APIRouter(prefix="/experiencias", tags=["Experiencias"])

async def get_current_regular_user_with_options(request: Request):
    if request.method == "OPTIONS":
        return None
    return await get_current_regular_user()

async def get_current_user_with_options(request: Request):
    if request.method == "OPTIONS":
        return None
    return await get_current_user()

@router.post("/", response_model=schemas.Experiencia)
def create_experiencia(
    exp: schemas.ExperienciaCreate,
    db: Session = Depends(get_db),
    current_regular_user: dict = Depends(get_current_regular_user_with_options)
):
    created = functions.create_experiencia(db, exp)
    return created

@router.put("/{experiencia_id}", response_model=schemas.Experiencia)
def update_experiencia(
    experiencia_id: int,
    experiencia_update: schemas.ExperienciaUpdate,
    db: Session = Depends(get_db),
    current_regular_user: dict = Depends(get_current_regular_user_with_options)
):
    updated = functions.update_experiencia(db, experiencia_id, experiencia_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Experiencia não encontrada")
    return updated

@router.delete("/{experiencia_id}", response_model=schemas.Experiencia)
def delete_experiencia(
    experiencia_id: int,
    db: Session = Depends(get_db),
    current_regular_user: dict = Depends(get_current_regular_user_with_options)
):
    deleted = functions.delete_experiencia(db, experiencia_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Experiencia não encontrada")
    return deleted

@router.get("/user/{user_id}", response_model=list[schemas.Experiencia])
def list_experiencias(user_id: int, db: Session = Depends(get_db)):
    experiencias = functions.get_experiencias_by_user(db, user_id)
    return experiencias