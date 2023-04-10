import asyncio
from typing import List

from aiohttp import ClientSession

from utils import *


async def fetch_problem(session: ClientSession, url: str) -> str | None:
    async with session.get(url) as resp:
        log.info(f"{resp.status} {resp.reason} {resp.url}")
        if resp.status != 200:
            resp.raise_for_status()
        else:
            return await resp.text()


async def fetch_all_problems(session: ClientSession) -> List:
    tasks = [
        asyncio.create_task(fetch_problem(session, PROJECT_EULER_URL % i))
        for i in range(1, 51)
    ]
    return await asyncio.gather(*tasks)


async def main():
    if not (dir_path := init_dir()):
        exit(1)
    euler_parser = EulerMinimalParser()
    async with ClientSession() as session:
        async with session.get(RESULTS_URL) as resp:
            log.info(f"{resp.status} {resp.reason} {resp.url}")
            results = parse_results(await resp.text()) or {}

        for i, raw_problem in enumerate(await fetch_all_problems(session)):
            euler_parser.feed(raw_problem)
            result_value = results.get(i)
            result = "" if not result_value else f"\nexpected result: {result_value}\n"
            write_problem(
                dir_path.joinpath(f"problem{i}.txt"),
                f"Problem #{i}\n{euler_parser.get_problem()}\n{result}",
            )
            pass


if __name__ == "__main__":
    asyncio.run(main())
