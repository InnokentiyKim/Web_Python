import aiohttp
import asyncio


async def main():
    session = aiohttp.ClientSession()

    response = await session.get(
        "http://127.0.0.1:8080/user/1"
    )
    print(response.status)
    print(await response.text())

    await session.close()


asyncio.run(main())