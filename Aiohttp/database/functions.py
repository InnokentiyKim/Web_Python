from aiohttp.web import HTTPNotFound, HTTPConflict
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from utils.errors import generate_error
from models.user import User
from models.adv import Adv


async def get_user_by_id(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if user is None:
        raise generate_error(HTTPNotFound, "user not found")
    return user

async def add_user(session: AsyncSession, user: User):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise generate_error(HTTPConflict, "user already exists")


async def get_adv_by_id(session: AsyncSession, adv_id: int):
    adv = await session.get(Adv, adv_id)
    if adv is None:
        raise generate_error(HTTPNotFound, "advertisement not found")
    return adv

async def add_adv(session: AsyncSession, adv: Adv):
    session.add(adv)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise generate_error(HTTPConflict, "advertisement already exists")
