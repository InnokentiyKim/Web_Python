from aiohttp import web
from models.adv import Adv


class AdvView(web.View):

    @property
    def adv_id(self):
        return self.request.match_info['adv_id']

    async def get(self):
        pass

    async def post(self):
        pass

    async def patch(self):
        pass

    async def delete(self):
        pass
