from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions

router = APIRouter(prefix="/vagas", tags=["Vagas"])

@router.post("/", response_model=schemas.Vaga)
def create_vaga(vaga: schemas.VagaCreate, db: Session = Depends(get_db)):
    return functions.create_vagaemprego(db, vaga)

@router.put("/vagas/{vaga_id}", response_model=schemas.VagaUpdate)
def update_vaga(vaga_id: int, vaga_update: schemas.VagaUpdate, db: Session = Depends(get_db)):
    updated = functions.update_vaga(db, vaga_id, vaga_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return updated

@router.delete("/vagas/{vaga_id}", response_model=schemas.Empresa)
def delete_vaga(vaga_id: int, db: Session = Depends(get_db)):
    deleted = functions.delete_vaga(db, vaga_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return deleted

@router.get("/empresa/{empresa_id}", response_model=list[schemas.Vaga])
def list_vagas_by_empresa(empresa_id: int, db: Session = Depends(get_db)):
    vagas = functions.get_vagas_by_empresa(db, empresa_id)
    if not vagas:
        raise HTTPException(status_code=404, detail="No vagas found for this empresa")
    return vagas

@router.post("/{vaga_id}/apply/{user_id}")
def apply_to_vaga(vaga_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        from app.user import functions as user_functions
        result = user_functions.apply_to_vaga(db, user_id, vaga_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/{vaga_id}/competencias/{competencia_id}")
def add_competencia(vaga_id: int, competencia_id: int, db: Session = Depends(get_db)):
    return functions.add_competencia_to_vaga(db, vaga_id, competencia_id)

@router.delete("/{vaga_id}/competencias/{competencia_id}")
def remove_competencia(vaga_id: int, competencia_id: int, db: Session = Depends(get_db)):
    return functions.remove_competencia_from_vaga(db, vaga_id, competencia_id)

@router.get("/{vaga_id}/competencias")
def list_competencias(vaga_id: int, db: Session = Depends(get_db)):
    return functions.get_vaga_competencias(db, vaga_id)