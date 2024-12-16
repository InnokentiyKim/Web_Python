import json
from aiohttp import web
from aiohttp.web import HTTPNotFound, HTTPConflict
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models import Session, User, init_orm, close_orm


def validate(json_data):
    return json_data


def generate_error(error_cls, message):
    error = error_cls(text=json.dumps({"error": message}), content_type="application/json")
    return error


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

app = web.Application(middlewares=[session_middleware])
app.cleanup_ctx.append(orm_context)


class UserView(web.View):

    @property
    def user_id(self):
        return int(self.request.match_info['user_id'])

    async def get(self):
        user = await get_user_by_id(self.request.session, self.user_id)
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()
        validated_data = validate(json_data)
        user = User(**validated_data)
        await add_user(self.request.session, user)
        return web.json_response(user.id_dict)

    async def patch(self):
        json_data = await self.request.json()
        validated_data = validate(json_data)
        user = await get_user_by_id(self.request.session, self.user_id)
        for field, value in validated_data.items():
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
        web.post("/user", UserView),
        web.patch("/user/{user_id:[0-9]+}", UserView),
        web.delete("/user/{user_id:[0-9]+}", UserView),
    ]
)



if __name__ == "__main__":
    web.run_app(app)
