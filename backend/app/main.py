from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, Base
from app.model import models
from app.admin.router import router as admin_router
from app.user.router import router as user_router
from app.empresa.router import router as empresa_router
from app.vagas.router import router as vagas_router
from app.experiencia.router import router as experiencias_router
from app.competencia.router import router as competencias_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://jobscout-frontend-production.up.railway.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

Base.metadata.create_all(bind=engine)

# Routers

app.include_router(admin_router)
app.include_router(user_router)
app.include_router(empresa_router)
app.include_router(vagas_router)
app.include_router(experiencias_router)
app.include_router(competencias_router)