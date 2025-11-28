from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from app.database import get_db
from . import schemas, functions
from app.model import models
from app.dependencies.auth import get_current_admin, get_current_user, get_current_regular_user

router = APIRouter(prefix="/vagas", tags=["Vagas"])

@router.post("/", response_model=schemas.Vaga)
def create_vaga(vaga: schemas.VagaCreate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    created = functions.create_vagaemprego(db, vaga)
    return created

@router.put("/{vaga_id}", response_model=schemas.Vaga)
def update_vaga(vaga_id: int, vaga_update: schemas.VagaUpdate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    updated = functions.update_vaga(db, vaga_id, vaga_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return updated

@router.delete("/{vaga_id}", response_model=schemas.Vaga)
def delete_vaga(vaga_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    deleted = functions.delete_vaga(db, vaga_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return deleted

@router.get("/", response_model=list[schemas.Vaga])
def list_vagas(db: Session = Depends(get_db)):
    return functions.get_vagas(db)

@router.get("/empresa/{empresa_id}", response_model=list[schemas.Vaga])
def list_vagas_by_empresa(empresa_id: int, db: Session = Depends(get_db)):
    vagas = functions.get_vagas_by_empresa(db, empresa_id)
    if not vagas:
        raise HTTPException(status_code=404, detail="No vagas found for this empresa")
    return vagas

@router.post("/{vaga_id}/apply/{user_id}")
def apply_to_vaga(vaga_id: int, user_id: int, db: Session = Depends(get_db), current_regular_user: dict = Depends(get_current_regular_user)):
    try:
        from app.user import functions as user_functions
        result = user_functions.apply_to_vaga(db, user_id, vaga_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/{vaga_id}/competencias/{competencia_id}")
def add_competencia(vaga_id: int, competencia_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    added = functions.add_competencia_to_vaga(db, vaga_id, competencia_id)
    return added

@router.delete("/{vaga_id}/competencias/{competencia_id}")
def remove_competencia(vaga_id: int, competencia_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    deleted = functions.remove_competencia_from_vaga(db, vaga_id, competencia_id)
    return deleted

@router.delete("/{vaga_id}/competencias", response_model=schemas.Vaga)
def clear_competencias(vaga_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    cleared = functions.clear_vaga_competencias(db, vaga_id)
    if not cleared:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return cleared

@router.get("/{vaga_id}/competencias")
def list_competencias(vaga_id: int, db: Session = Depends(get_db), all_users: dict = Depends(get_current_user)):
    return functions.get_vaga_competencias(db, vaga_id)

@router.get("/admin-with-applications", response_model=list[schemas.VagaWithUsers])
def get_vagas_application_for_admin(db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    return functions.get_vagas_with_applications_for_admin(db, current_admin["id"])

@router.get("/admin", response_model=list[schemas.Vaga])
def get_vagas_for_admin(db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    admin_id = current_admin["id"]
    vagas = functions.get_vagas_by_admin(db, admin_id)
    return vagas