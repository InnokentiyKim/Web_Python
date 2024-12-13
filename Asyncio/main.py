import datetime
import asyncio
import aiohttp
import more_itertools
from models import init_orm, close_orm
from constants import MAX_COROS, PARAMS_LIST, EXTRA_PARAMS
from async_requests import get_people_count, get_people, adapt_people_json, insert_people


async def main():
    await init_orm()
    async with aiohttp.ClientSession(trust_env=True) as http_session:
        amount = await get_people_count(http_session)
        for i_list in more_itertools.chunked(range(1, amount), MAX_COROS):
            coros = [get_people(i, http_session) for i in i_list]
            people_json = await asyncio.gather(*coros)
            title_coros = [adapt_people_json(person, http_session, PARAMS_LIST, EXTRA_PARAMS) for person in people_json]
            result = await asyncio.gather(*title_coros)
            task = asyncio.create_task(insert_people(result))
        tasks = asyncio.all_tasks()
        tasks.remove(asyncio.current_task())
        await asyncio.gather(*tasks)
    await close_orm()


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)