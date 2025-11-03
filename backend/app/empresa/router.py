from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.post("/", response_model=schemas.Empresa)
def register_admin(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    return functions.create_empresa(db, empresa)

@router.put("/empresas/{empresa_id}", response_model=schemas.Empresa)
def update_empresa(empresa_id: int, empresa_update: schemas.EmpresaUpdate, db: Session = Depends(get_db)):
    updated = functions.update_empresa(db, empresa_id, empresa_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return updated

@router.delete("/empresas/{empresa_id}", response_model=schemas.Empresa)
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    deleted = functions.delete_empresa(db, empresa_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return deleted

@router.get("/", response_model=list[schemas.Empresa])
def list_empresas(db: Session = Depends(get_db)):
    return functions.get_empresas(db)