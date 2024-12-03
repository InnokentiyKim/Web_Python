import datetime
import asyncio
import aiohttp
import more_itertools
from models import SwapiPeople, Session, init_orm, close_orm

MAX_COROS = 10

async def get_people(person_id: int, http_session):
    url = f"http://swapi.py4e.com/api/people/{person_id}/"
    http_response = await http_session.get(url)
    json_data = await http_response.json()
    return json_data

async def insert_people(json_data: list[dict] | tuple[dict]):
    async with Session() as session:
        swapi_people_list = [SwapiPeople(json=item) for item in json_data]
        session.add_all(swapi_people_list)
        await session.commit()
    

async def main():
    await init_orm()
    async with aiohttp.ClientSession() as http_session:
        for i_list in more_itertools.chunked(range(1, 101), MAX_COROS):
            coros = [get_people(i, http_session) for i in i_list]
            result = await asyncio.gather(*coros)
            coro = insert_people(result)
            task = asyncio.create_task(coro)
    await close_orm()
    
if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)