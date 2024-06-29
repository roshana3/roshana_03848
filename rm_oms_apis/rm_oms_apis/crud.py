from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        user_role=user.user_role,
        status=user.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_status(db: Session, email: str, status: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    user.status = status
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    db.delete(user)
    db.commit()
    return user
