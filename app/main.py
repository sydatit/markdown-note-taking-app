from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# from models import models
from . import models
from .database import SessionLocal, engine
from . import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/users", response_model=List[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
