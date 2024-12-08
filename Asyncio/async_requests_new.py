import datetime
import asyncio
import aiohttp


MAX_COROS = 10

async def get_people(person_id: int, http_session):
    url = f"http://swapi.py4e.com/api/people/{person_id}/"
    http_response = await http_session.get(url)
    json_data = await http_response.json()
    return json_data




async def main():
    async with aiohttp.ClientSession() as http_session:
        coro_1 = get_people(1, http_session)
        coro_2 = get_people(2, http_session)
        coro_3 = get_people(3, http_session)
        result = await asyncio.gather(coro_1, coro_2, coro_3)
    print(result)


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)