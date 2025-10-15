from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, Base
from app.model import models
from app.admin.router import router as admin_router
from app.user.router import router as user_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

Base.metadata.create_all(bind=engine)

# Routers

app.include_router(admin_router)
app.include_router(user_router)