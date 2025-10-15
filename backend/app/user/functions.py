from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.model import models
from . import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_cpf(db: Session, cpf: str):
    return db.query(models.User).filter(models.User.cpf == cpf).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(
        nome=user.nome,
        email=user.email,
        cpf=user.cpf,
        telefone=user.telefone,
        hashed_password=hashed_pw,
        area_trabalho=user.area_trabalho,
        nivel_educacao=user.nivel_educacao
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()
