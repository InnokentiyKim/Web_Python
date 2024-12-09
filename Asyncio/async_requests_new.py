import datetime
import asyncio
import aiohttp
import more_itertools
from models import SwapiPeople, Session, init_orm, close_orm


MAX_COROS = 10


async def get_people_count(http_session):
    url = f"http://swapi.py4e.com/api/people/"
    http_response = await http_session.get(url)
    json_data = await http_response.json()
    return json_data.get("count", 0)


async def get_param_from_link(http_session: Session, link: str, param: str) -> str:
    http_response = await http_session.get(link)
    json_data = await http_response.json()
    return json_data.get(param, "")


async def get_people(person_id: int, http_session):
    url = f"http://swapi.py4e.com/api/people/{person_id}/"
    http_response = await http_session.get(url)
    json_data = await http_response.json()
    return json_data


async def insert_people(json_list: list[dict] | tuple[dict]):
    async with Session() as session:
        swapi_people_list = [SwapiPeople(**item) for item in json_list]
        session.add_all(swapi_people_list)
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as http_session:
        amount = await get_people_count(http_session)
        for i_list in more_itertools.chunked(range(1, amount), MAX_COROS):
            coros = [get_people(i, http_session) for i in i_list]
            result = await asyncio.gather(*coros)
            task = asyncio.create_task(insert_people(result))
        tasks = asyncio.all_tasks()
        tasks.remove(asyncio.current_task())
        await asyncio.gather(*tasks)
    await close_orm()


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
