from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/empresas", tags=["Empresas"])

async def get_current_admin_with_options(request: Request):
    if request.method == "OPTIONS":
        return None
    return await get_current_admin()

@router.post("/", response_model=schemas.Empresa)
def create_empresa(
    empresa: schemas.EmpresaCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin_with_options)
):
    return functions.create_empresa(db, empresa)

@router.put("/{empresa_id}", response_model=schemas.Empresa)
def update_empresa(
    empresa_id: int,
    empresa_update: schemas.EmpresaUpdate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin_with_options)
):
    updated = functions.update_empresa(db, empresa_id, empresa_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return updated

@router.delete("/{empresa_id}", response_model=schemas.Empresa)
def delete_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin_with_options)
):
    deleted = functions.delete_empresa(db, empresa_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return deleted

@router.get("/", response_model=list[schemas.Empresa])
def list_empresas(db: Session = Depends(get_db)):
    return functions.get_empresas(db)

@router.get("/admin", response_model=list[schemas.Empresa])
def get_empresas_for_admin(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin_with_options)
):
    empresas = functions.get_empresas_by_admin(db, current_admin["id"])
    return empresas