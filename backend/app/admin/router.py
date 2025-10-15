from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.admin import schemas, functions

router = APIRouter(prefix="/admins", tags=["Admins"])

@router.post("/", response_model=schemas.Admin)
def register_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    if functions.get_admin_by_email(db, admin.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if functions.get_admin_by_cpf(db, admin.cpf):
        raise HTTPException(status_code=400, detail="CPF already registered")
    return functions.create_admin(db, admin)