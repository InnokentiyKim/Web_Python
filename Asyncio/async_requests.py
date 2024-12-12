import datetime
import asyncio
import aiohttp
import more_itertools
from models import SwapiPeople, Session, init_orm, close_orm
from sqlalchemy.exc import IntegrityError


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
    url = f"https://swapi.py4e.com/api/people/"
    http_response = await http_session.get(url, ssl=False)
    json_data = await http_response.json()
    people_count = json_data.get('count', 0)
    return int(people_count)


async def get_titles_from_links(http_session, links: list[str] | str, target_param: str) -> str:
    if type(links) == str:
        links = [links]
    param_titles = []
    for link in links:
        http_response = await http_session.get(link, ssl=False)
        json_data = await http_response.json()
        title = json_data.get(target_param, "")
        param_titles.append(title)
    return ", ".join(param_titles)


async def get_people(person_id: int, http_session):
    url = f"https://swapi.py4e.com/api/people/{person_id}/"
    http_response = await http_session.get(url, ssl=False)
    json_data = await http_response.json()
    return json_data


async def adapt_people_json(json_data: dict, http_session, params_list: list[str], extra_params: dict[str, str]) -> dict:
    result_dict = {}
    for param in params_list:
        if param in extra_params:
            target_param = extra_params[param]
            links_list = json_data.get(param, [])
            title = await get_titles_from_links(http_session, links_list, target_param)
            result_dict[param] = title
        else:
            result_dict[param] = json_data.get(param, "")
    return result_dict


async def insert_people(json_list: list[dict] | tuple[dict]):
    async with Session() as session:
        swapi_people_list = [SwapiPeople(**item) for item in json_list]
        session.add_all(swapi_people_list)
        try:
            await session.commit()
        except IntegrityError:
            print(f"Person or People already exists in database: {json_list}")
            await session.rollback()



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
