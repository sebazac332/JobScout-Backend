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

def get_admins(db: Session):
    return db.query(models.Admin).all()
