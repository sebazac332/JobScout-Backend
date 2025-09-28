from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, Base, get_db

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

Base.metadata.create_all(bind=engine)

# Admins

@app.post("/admins/", response_model=schemas.Admin)
def register_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    if crud.get_admin_by_email(db, admin.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if crud.get_admin_by_cpf(db, admin.cpf):
        raise HTTPException(status_code=400, detail="CPF already registered")
    return crud.create_admin(db, admin)

@app.get("/admins/", response_model=list[schemas.Admin])
def list_admins(db: Session = Depends(get_db)):
    return crud.get_admins(db)