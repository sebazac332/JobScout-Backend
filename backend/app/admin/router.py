from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, functions
from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/admins", tags=["Admins"])

@router.post("/", response_model=schemas.Admin)
def register_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    if functions.get_admin_by_email(db, admin.email):
        raise HTTPException(status_code=400, detail="Email já registrado")
    if functions.get_admin_by_cpf(db, admin.cpf):
        raise HTTPException(status_code=400, detail="CPF já registrado")
    return functions.create_admin(db, admin)

@router.put("/{admin_id}", response_model=schemas.Admin)
def edit_admin(admin_id: int, admin_update: schemas.AdminUpdate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    admin = functions.update_admin(db, admin_id, admin_update)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return admin

@router.delete("/{admin_id}", response_model=schemas.Admin)
def remove_admin(admin_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    admin = functions.delete_admin(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return admin

@router.get("/me", response_model=schemas.Admin)
def get_me(current_admin=Depends(get_current_admin)):
    return current_admin