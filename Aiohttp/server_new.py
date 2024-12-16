from aiohttp import web
from utils.application import session_middleware, orm_context
from views.user_view import UserView


app = web.Application(middlewares=[session_middleware])
app.cleanup_ctx.append(orm_context)


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
