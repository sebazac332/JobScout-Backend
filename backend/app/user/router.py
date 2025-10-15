from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.user import schemas, functions

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if functions.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if functions.get_user_by_cpf(db, user.cpf):
        raise HTTPException(status_code=400, detail="CPF already registered")
    return functions.create_user(db, user)