import atexit
import os
from flask import request
from sqlalchemy.exc import IntegrityError
from models import Adv, Base, User
from utils.http_error import HttpError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5430")

DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)
Base.metadata.create_all(bind=engine)

def get_adv_by_id(adv_id: int):
    adv = request.session.get(Adv, adv_id)
    if not adv:
        raise HttpError(status_code=404, err_message="advertisement not found")
    return adv


def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    if not user:
        raise HttpError(status_code=404, err_message="user not found")
    return user


def add_adv(adv: Adv):
    request.session.add(adv)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(status_code=409, err_message="advertisement already exists")
    
    
def add_user(user: User):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(status_code=409, err_message="user already exists")
    