import asyncio

import aiohttp


async def main():
    session = aiohttp.ClientSession()

    response = await session.post(
        "http://127.0.0.1:8080/user", json={"name": "user_1", "password": "12345678"}
    )
    print(response.status)
    print(await response.json())

    response = await session.get("http://127.0.0.1:8080/user/1")
    print(response.status)
    print(await response.text())

    response = await session.patch(
        "http://127.0.0.1:8080/user/1", json={"name": "new_username"}
    )
    print(response.status)
    print(await response.json())

    response = await session.get("http://127.0.0.1:8080/user/1")
    print(response.status)
    print(await response.text())

    response = await session.delete("http://127.0.0.1:8080/user/1")
    print(response.status)
    print(await response.text())

    response = await session.get("http://127.0.0.1:8080/user/1")
    print(response.status)
    print(await response.text())

    ###################################

    response = await session.post(
        "http://127.0.0.1:8080/adv",
        json={
            "title": "first advertisement",
            "description": "first simple description",
            "owner": 1,
        },
    )
    print(response.status)
    print(await response.json())

    response = await session.get("http://127.0.0.1:8080/adv/1")
    print(response.status)
    print(await response.text())

    response = await session.patch(
        "http://127.0.0.1:8080/adv/1",
        json={
            "description": "description updated",
        },
    )
    print(response.status)
    print(await response.json())

    response = await session.get("http://127.0.0.1:8080/adv/1")
    print(response.status)
    print(await response.text())

    response = await session.delete("http://127.0.0.1:8080/adv/1")
    print(response.status)
    print(await response.text())

    response = await session.get("http://127.0.0.1:8080/adv/1")
    print(response.status)
    print(await response.text())

    await session.close()


asyncio.run(main())
