from aiohttp import web

from database.functions import add_adv, get_adv_by_id
from models.adv import Adv
from schemas.adv_schema import CreateAdv, UpdateAdv
from utils.validation import validate


class AdvView(web.View):

    @property
    def adv_id(self):
        return int(self.request.match_info["adv_id"])

    async def get(self):
        adv = await get_adv_by_id(self.request.session, self.adv_id)
        return web.json_response(adv.dict)

    async def post(self):
        json_data = await self.request.json()
        validated_data = validate(json_data, CreateAdv)
        adv = Adv(**validated_data)
        await add_adv(self.request.session, adv)
        return web.json_response(adv.id_dict)

    async def patch(self):
        json_data = await self.request.json()
        validated_data = validate(json_data, UpdateAdv)
        adv = await get_adv_by_id(self.request.session, self.adv_id)
        for field, value in validated_data.items():
            setattr(adv, field, value)
        await add_adv(self.request.session, adv)
        return web.json_response(adv.id_dict)

    async def delete(self):
        adv = await get_adv_by_id(self.request.session, self.adv_id)
        await self.request.session.delete(adv)
        await self.request.session.commit()
        return web.json_response({"status": "deleted"})
