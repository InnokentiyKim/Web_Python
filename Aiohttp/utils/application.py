from aiohttp import web

from database.settings import Session
from models.base import close_orm, init_orm


async def orm_context(app: web.Application):
    print("START")
    await init_orm()
    yield
    await close_orm()
    print("END")


@web.middleware
async def session_middleware(request, handler):
    async with Session() as session:
        request.session = session
        result = await handler(request)
        return result
