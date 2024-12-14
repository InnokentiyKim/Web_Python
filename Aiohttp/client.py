import aiohttp
import asyncio


async def main():
    session = aiohttp.ClientSession()

    response = await session.post(
        "http://127.0.0.1:8080/hello/world/42?k=1&v=2",
        json={"name": "Inncent"},
        headers={"token": "xxxxxxxxx"},
    )
    print(response.status)
    print(await response.text())

    await session.close()


asyncio.run(main())