import datetime
import asyncio
import aiohttp
import more_itertools
from models import SwapiPeople, Session, init_orm, close_orm
from schema import SwapiPeopleSchema, validate_json


MAX_COROS = 10

EXTRA_PARAMS = [
    'films',
    'homeworld',
    'species',
    'starships',
    'vehicles',
]

async def get_people_count(http_session):
    url = f"http://swapi.py4e.com/api/people/"
    http_response = await http_session.get(url)
    json_data = await http_response.json()
    return json_data.get("count", 0)


async def get_param_from_links(http_session: Session, links_list: list[str], param: str) -> str:
    param_str_list = []
    for link in links_list:
        http_response = await http_session.get(link)
        json_data = await http_response.json()
        param_str = json_data.get(param, "")
        param_str_list.append(param_str)
    return ", ".join(param_str_list)


async def get_people(person_id: int, http_session, extra_params: list[str]):
    url = f"http://swapi.py4e.com/api/people/{person_id}/"
    http_response = await http_session.get(url)
    json_data = await http_response.json()
    extra_params_dict = {}
    for param in extra_params:
        links_list = json_data.get(param, [])
        extra_params_dict[param] = await get_param_from_links(http_session, links_list, param)
        json_data[param] = extra_params_dict[param]
    validated_data = validate_json(json_data, SwapiPeopleSchema)
    return validated_data


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
            coros = [get_people(i, http_session, EXTRA_PARAMS) for i in i_list]
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
