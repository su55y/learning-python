import asyncio
from typing import List, Optional

from aiohttp import ClientSession

from utils import log, ProblemsHandler, PROJECT_EULER_URL, RESULTS_URL


async def fetch_problem(session: ClientSession, url: str) -> Optional[str]:
    async with session.get(url) as resp:
        log.info(f"{resp.status} {resp.reason} {resp.url}")
        if resp.status == 200:
            return await resp.text()


async def fetch_all_problems(session: ClientSession) -> List[str]:
    tasks = [
        asyncio.create_task(fetch_problem(session, PROJECT_EULER_URL % i))
        for i in range(1, 51)
    ]
    return await asyncio.gather(*tasks)


async def main():
    async with ClientSession() as session:
        results = ""
        async with session.get(RESULTS_URL) as resp:
            log.info(f"{resp.status} {resp.reason} {resp.url}")
            results = await resp.text()
        problems = await fetch_all_problems(session)
        h = ProblemsHandler(raw_results=results, raw_problems=problems)
        h.write_problems()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(repr(e))
