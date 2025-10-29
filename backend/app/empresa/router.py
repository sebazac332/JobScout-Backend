from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.post("/", response_model=schemas.Empresa)
def register_admin(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    return functions.create_empresa(db, empresa)

@router.get("/", response_model=list[schemas.Empresa])
def list_empresas(db: Session = Depends(get_db)):
    return functions.get_empresas(db)