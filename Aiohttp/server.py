from aiohttp import web
from models import init_orm, close_orm


app = web.Application()


async def orm_context(app: web.Application):
    print("START")
    await init_orm()
    yield
    await close_orm()
    print("END")


app.cleanup_ctx.append(orm_context)


async def hello_world(request: web.Request):
    some_id = int(request.match_info["some_id"])
    qs = request.query
    headers = request.headers
    json_data = await request.json()
    print(f"{some_id=}, {qs=}, {headers=}, {json_data=}")
    return web.json_response({"hello": "world"})


app.add_routes([
    web.post('/hello/world/{some_id:[0-9]+}', hello_world)
])

web.run_app(app)