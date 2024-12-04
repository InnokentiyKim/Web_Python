from flask import request, g
from sqlalchemy import select
from models import User
from app_base import auth, bcrypt


def hash_password(password: str) -> str:
    password_bytes = password.encode()
    password_hashed_bytes = bcrypt.generate_password_hash(password_bytes)
    password_hashed_string = password_hashed_bytes.decode()
    return password_hashed_string


@auth.verify_password
def verify_pwd(username: str, password: str) -> bool:
    query = select(User).filter_by(name=username)
    user = request.session.execute(query).scalars().first()
    if user is None or not bcrypt.check_password_hash(user.password, password):
        return False
    g.user = user
    return True