from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.model import models
from . import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_admin_by_email(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()

def get_admin_by_cpf(db: Session, cpf: str):
    return db.query(models.Admin).filter(models.Admin.cpf == cpf).first()

def create_admin(db: Session, admin: schemas.AdminCreate):
    hashed_pw = pwd_context.hash(admin.password)
    db_admin = models.Admin(
        nome=admin.nome,
        email=admin.email,
        cpf=admin.cpf,
        telefone=admin.telefone,
        hashed_password=hashed_pw
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def update_admin(db: Session, admin_id: int, admin_update: schemas.AdminUpdate):
    db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()

    if not db_admin:
        return None

    if admin_update.nome is not None:
        db_admin.nome = admin_update.nome
    if admin_update.email is not None:
        db_admin.email = admin_update.email
    if admin_update.cpf is not None:
        db_admin.cpf = admin_update.cpf
    if admin_update.telefone is not None:
        db_admin.telefone = admin_update.telefone
    if admin_update.password is not None:
        db_admin.hashed_password = pwd_context.hash(admin_update.password)

    db.commit()
    db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, admin_id: int):
    db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()

    if not db_admin:
        return None 

    db.delete(db_admin)
    db.commit()
    return db_admin

def get_admins(db: Session):
    return db.query(models.Admin).all()
