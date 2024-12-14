from aiohttp import web
from aiohttp.web import HTTPNotFound
from models import init_orm, close_orm, Session, User
from sqlalchemy.ext.asyncio import AsyncSession
import json


def generate_error(error_cls, message):
    error = error_cls(text=json.dumps({"error": message}), content_type="application/json")
    return error


async def get_user_by_id(session: AsyncSession, user_id):
    user = await session.get(User, user_id)
    if user is None:
        raise generate_error(HTTPNotFound, "user not found")
    return user


app = web.Application()


async def orm_context(app: web.Application):
    print("START")
    await init_orm()
    yield
    await close_orm()
    print("END")


@web.middleware
async def session_middleware(request, handler):
    async with Session() as session:
        print("before request")
        request.session = session
        result = await handler(request)
        print("after request")
        return result

app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


async def hello_world(request: web.Request):
    some_id = int(request.match_info["some_id"])
    qs = request.query
    headers = request.headers
    json_data = await request.json()
    print(f"{some_id=}, {qs=}, {headers=}, {json_data=}")
    return web.json_response({"hello": "world"})


class UserView(web.View):
    async def get(self):
        user_id = int(self.request.match_info["user_id"])
        user = await get_user_by_id(self.request.session, user_id)
        return web.json_response(user.dict)


    async def post(self):
        pass

    async def patch(self):
        pass

    async def delete(self):
        pass


app.add_routes([
    web.get('/user/{user_id:[0-9]+}', UserView),
    web.patch('/user/{user_id:[0-9]+}', UserView),
    web.delete('/user/{user_id:[0-9]+}', UserView),
    web.post('/user', UserView),
])

web.run_app(app)