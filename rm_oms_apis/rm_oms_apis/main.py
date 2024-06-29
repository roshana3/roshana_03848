from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth, dependencies
from .database import engine, SessionLocal
from typing import List
from datetime import datetime, timedelta
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

fake_users_db = {}

@app.post("/signup/", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login1/")
def login(form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials or user not found")
    return {"access_token": auth.create_access_token(user.email), "token_type": "bearer"}

@app.post("/login/", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(dependencies.get_db), form_data: auth.OAuth2PasswordRequestForm = Depends()):
    # user = crud.get_user_by_email(db, email=form_data.username)
    user = auth.authenticate_user2(db, form_data.username, form_data.password)
    # user = auth.authenticate_user(fake_users_db, form_data.username, form_data.password)

    print("passowrd:",form_data.password)
    print("passowrd:",form_data.username)
    print("passowrd: h",user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.status == "pending":
        raise HTTPException(status_code=201, detail="Your registration is pending approval")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"user":user,"access_token": access_token, "token_type": "bearer"}


@app.get("/users/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.delete("/users/{email}", response_model=schemas.UserBase)
def delete_user(email: str, db: Session = Depends(dependencies.get_db)):
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, email=email)

@app.post("/approve_user/{email}", response_model=schemas.UserBase)
def approve_user(email: str, db: Session = Depends(dependencies.get_db)):
    user = crud.update_user_status(db, email=email, status="approved")

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# @app.post("/admin/users/{user_id}/approve/", response_model=schemas.UserResponse)
# def approve_user(user_id: int, db: Session = Depends(dependencies.get_db), current_user: schemas.UserResponse = Depends(auth.get_current_admin_user)):
#     user = crud.update_user_status(db, user_id=user_id, status="approved")
#     return user

