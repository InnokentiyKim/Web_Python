from flask import request, g
from sqlalchemy import select
from models import User
from app_base import auth, bcrypt
from utils.http_error import HttpError


def hash_password(password: str) -> str:
    password_bytes = password.encode()
    password_hashed_bytes = bcrypt.generate_password_hash(password_bytes)
    password_hashed_string = password_hashed_bytes.decode()
    return password_hashed_string


def is_owner_or_raise_error(user_id: int, owner_id: int) -> bool:
    if user_id != owner_id:
        raise HttpError(status_code=403, err_message="Forbidden")
    return True


@auth.verify_password
def verify_pwd(username: str, password: str) -> bool:
    query = select(User).filter_by(name=username)
    user = request.session.execute(query).scalars().first()
    if user is None or not bcrypt.check_password_hash(user.password, password):
        return False
    g.user = user
    return True