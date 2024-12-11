import datetime
import asyncio
import aiohttp
import more_itertools
from models import SwapiPeople, Session, init_orm, close_orm
from schema import SwapiPeopleSchema, validate_json


MAX_COROS = 10

PARAMS_LIST = [
    'name',
    'birth_year',
    'eye_color',
    'films',
    'gender',
    'hair_color',
    'height',
    'mass',
    'skin_color',
    'homeworld',
    'species',
    'starships',
    'vehicles',
]

EXTRA_PARAMS = {
    'homeworld': 'name',
    'films': 'title',
    'species': 'name',
    'starships': 'name',
    'vehicles': 'name',
}

async def get_people_count(http_session) -> int:
    url = f"http://swapi.py4e.com/api/people/"
    http_response = await http_session.get(url)
    json_data = await http_response.json()
    people_count = json_data.get('count', 0)
    return int(people_count)


async def get_param_from_links(http_session, links: list[str] | str, param_name: str) -> str:
    if type(links) == str:
        links = [links]
    param_str_list = []
    for link in links:
        http_response = await http_session.get(link, ssl=False)
        json_data = await http_response.json()
        param_str = json_data.get(param_name, "")
        param_str_list.append(param_str)
    return ", ".join(param_str_list)


async def get_people(person_id: int, http_session, extra_params: dict[str, str]):
    url = f"https://swapi.py4e.com/api/people/{person_id}/"
    http_response = await http_session.get(url, ssl=False)
    json_data = await http_response.json()
    extra_params_dict = {}
    for param in extra_params:
        links_list = json_data.get(param, [])
        param_name = extra_params.get(param)
        extra_params_dict[param] = await get_param_from_links(http_session, links_list, param_name)
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
    async with aiohttp.ClientSession(trust_env=True) as http_session:
        amount = await get_people_count(http_session)
        for i_list in more_itertools.chunked(range(1, 10), MAX_COROS):
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
