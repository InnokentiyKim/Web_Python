from aiohttp import web

from database.functions import add_user, get_user_by_id
from models.user import User
from schemas.user_schema import CreateUser, UpdateUser
from utils.validation import validate


class UserView(web.View):

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get(self):
        user = await get_user_by_id(self.request.session, self.user_id)
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()
        validated_data = validate(json_data, CreateUser)
        user = User(**validated_data)
        await add_user(self.request.session, user)
        return web.json_response(user.id_dict)

    async def patch(self):
        json_data = await self.request.json()
        validated_data = validate(json_data, UpdateUser)
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
