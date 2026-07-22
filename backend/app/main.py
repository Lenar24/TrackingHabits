from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from . import models, schemas, crud
from .database import engine, get_db

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API")

@app.get("/")
def read_root():
    return {"message": "Habit Tracker API is running"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/habits/", response_model=schemas.Habit)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    return crud.create_habit(db=db, habit=habit)

@app.get("/habits/{user_id}", response_model=List[schemas.Habit])
def get_habits(user_id: int, db: Session = Depends(get_db)):
    return crud.get_habits(db, user_id=user_id)

@app.put("/habits/{habit_id}/complete")
def complete_habit(habit_id: int, db: Session = Depends(get_db)):
    return crud.complete_habit(db, habit_id)
