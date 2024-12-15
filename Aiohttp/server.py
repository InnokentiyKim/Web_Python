import json

from aiohttp import web
from aiohttp.web import HTTPConflict, HTTPNotFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Session, User, close_orm, init_orm


def validate(json_data):
    return json_data


def generate_error(error_cls, message):
    error = error_cls(
        text=json.dumps({"error": message}), content_type="application/json"
    )
    return error


async def get_user_by_id(session: AsyncSession, user_id):
    user = await session.get(User, user_id)
    if user is None:
        raise generate_error(HTTPNotFound, "user not found")
    return user


async def add_user(session: AsyncSession, user: User):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        raise generate_error(HTTPConflict, "user already exists")


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

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get(self):
        user = await get_user_by_id(self.request.session, self.user_id)
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()
        json_data = validate(json_data)
        user = User(**json_data)
        await add_user(self.request.session, user)
        return web.json_response(user.id_dict)

    async def patch(self):
        json_data = await self.request.json()
        json_data = validate(json_data)
        user = await get_user_by_id(self.request.session, self.user_id)
        for field, value in json_data.items():
            setattr(user, field, value)
        await add_user(self.request.session, user)
        return web.json_response(user.id_dict)

    async def delete(self):
        user = await get_user_by_id(self.request.session, self.user_id)
        await self.request.session.delete(user)
        await self.request.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.get("/user/{user_id:[0-9]+}", UserView),
        web.patch("/user/{user_id:[0-9]+}", UserView),
        web.delete("/user/{user_id:[0-9]+}", UserView),
        web.post("/user", UserView),
    ]
)

web.run_app(app)
