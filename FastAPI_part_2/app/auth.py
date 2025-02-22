import bcrypt


def hash_password(password: str) -> str:
    password = password.encode()
    bcrypt.hashpw(password, bcrypt.gensalt())
    return password.decode()


def check_password(user_password: str, hashed_password_db: str) -> bool:
    user_password = user_password.encode()
    hashed_password_db = hashed_password_db.encode()
    return check_password(user_password, hashed_password_db)
