from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/competencias", tags=["Competencias"])

async def get_current_user_with_options(request: Request):
    if request.method == "OPTIONS":
        return None
    return await get_current_user()

@router.post("/", response_model=schemas.Competencia)
def create_competencia(
    competencia: schemas.CompetenciaCreate,
    db: Session = Depends(get_db),
    all_users: dict = Depends(get_current_user_with_options)
):
    return functions.create_competencia(db, competencia)

@router.delete("/{competencia_id}", response_model=schemas.Competencia)
def delete_competencia(
    competencia_id: int,
    db: Session = Depends(get_db),
    all_users: dict = Depends(get_current_user_with_options)
):
    deleted_competencia = functions.delete_competencia(db, competencia_id)
    if not deleted_competencia:
        raise HTTPException(status_code=404, detail="Competência não encontrada")
    return deleted_competencia

@router.get("/", response_model=list[schemas.Competencia])
def list_competencias(db: Session = Depends(get_db)):
    return functions.get_competencias(db)