from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException

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

def apply_to_vaga(db: Session, user_id: int, vaga_id: int):
    user = db.query(models.User).get(user_id)
    vaga = db.query(models.Vagaemprego).get(vaga_id)

    if not user or not vaga:
        raise HTTPException(status_code=404, detail="User or Vaga not found")

    if user in vaga.candidatos:
        raise HTTPException(status_code=400, detail="User already applied to this vaga")

    vaga.candidatos.append(user)
    db.commit()
    db.refresh(vaga)
    return {"message": "User applied successfully!"}

def add_competencia_to_user(db: Session, user_id: int, competencia_id: int):
    user = db.query(models.User).get(user_id)
    competencia = db.query(models.Competencia).get(competencia_id)

    if not user or not competencia:
        raise HTTPException(status_code=404, detail="Usuário ou competência não encontrado")

    if competencia in user.competencias:
        raise HTTPException(status_code=400, detail="Competência já associada ao usuário")

    user.competencias.append(competencia)
    db.commit()
    return {"message": "Competência adicionada ao usuário com sucesso"}


def remove_competencia_from_user(db: Session, user_id: int, competencia_id: int):
    user = db.query(models.User).get(user_id)
    competencia = db.query(models.Competencia).get(competencia_id)

    if not user or not competencia:
        raise HTTPException(status_code=404, detail="Usuário ou competência não encontrado")

    if competencia not in user.competencias:
        raise HTTPException(status_code=400, detail="Competência não associada ao usuário")

    user.competencias.remove(competencia)
    db.commit()
    return {"message": "Competência removida do usuário com sucesso"}

def get_user_competencias(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    return user.competencias