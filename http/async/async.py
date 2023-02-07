from html.parser import HTMLParser
from logging import info, error, basicConfig, INFO
from os import path, mkdir
from re import match
from textwrap import wrap
from typing import Dict, List, Tuple
from threading import Thread
from asyncio import gather, create_task, run

from aiohttp import ClientSession

PROJECT_EULER_URL = "https://projecteuler.net/minimal=%d"
RESULTS_URL = "https://raw.githubusercontent.com/zengin/project-euler-solutions/master/results.txt"

PROBLEMS_DIR_NAME = "problems"


class EulerMinimalParser(HTMLParser):
    _problem = ""

    def get_problem(self) -> str:
        problem_text = "".join([s for s in self._problem.splitlines(True) if s.strip()])
        problem_text = "\n".join(wrap(problem_text, 80, break_long_words=False)).strip()
        self._problem = ""
        return problem_text

    def handle_data(self, data):
        if len(data) > 0:
            self._problem = f"{self._problem}{data}\n"


def parse_results(raw_results: str) -> Dict[int, int]:
    results: Dict[int, int] = dict()
    for line in raw_results.split("\n"):
        if not match(r"^0\d{2}\:\s-?\d+$", line):
            continue
        index, result = line.replace(":", "").split()
        results[int(index, 10)] = int(result, 10)

    return results


def init_dir() -> bool:
    ABS_DIR_PATH = path.abspath(f"./{PROBLEMS_DIR_NAME}")
    if not path.exists(ABS_DIR_PATH):
        try:
            mkdir(ABS_DIR_PATH)
        except Exception as e:
            error(repr(e))
            return False
        else:
            info(f"{ABS_DIR_PATH} created")
    elif path.isdir(ABS_DIR_PATH):
        info(f"{ABS_DIR_PATH} already exists")

    return True


async def fetch_problem(
    index: int, url: str, session: ClientSession
) -> Tuple[int, str] | None:
    async with session.get(url) as resp:
        log = f"{resp.status} {resp.reason} {resp.url}"
        if resp.status != 200:
            error(log)
            resp.raise_for_status()
        else:
            info(log)
            t = await resp.text()
            return index, t


async def fetch_all_problems(session: ClientSession):
    tasks = []
    for i in range(1, 51):
        task = create_task(fetch_problem(i, PROJECT_EULER_URL % i, session))
        tasks.append(task)
    res = await gather(*tasks)
    return res


def write_problem(index: int, text: str, result: str):
    euler_parser = EulerMinimalParser()
    euler_parser.feed(text)
    path = f"{PROBLEMS_DIR_NAME}/problem{index}"
    try:
        with open(path, "w") as file:
            file.write(f"Problem #{index}\n{euler_parser.get_problem()}\n{result}")
    except Exception as e:
        error(repr(e))
    else:
        info(f"file written to {path}")


def write_problems(
    problems_list: List[Tuple[int, str]], results: Dict[int, int] | None
):
    for (index, text) in problems_list:
        result = None
        if results and index in results.keys():
            result = results.get(index)
        result = "" if not result else f"\nexpected result: {result}\n"
        p = Thread(target=write_problem, args=(index, text, result))
        p.start()


async def main():
    basicConfig(
        level=INFO,
        format="\x1b[38;5;44m%(asctime)s [%(levelname)s]:\x1b[0m %(message)s",
        datefmt="%H:%M:%S %d/%m/%y",
    )
    if not init_dir():
        exit(1)

    results = None
    problems_list: List[Tuple[int, str]] = list()

    async with ClientSession() as session:
        async with session.get(RESULTS_URL) as resp:
            log = f"{resp.status} {resp.reason} {resp.url}"
            if resp.status != 200:
                error(log)
            else:
                info(log)
                results = await resp.text()
                results = parse_results(results)

        problems_list = await fetch_all_problems(session)

    write_problems(problems_list, results)


if __name__ == "__main__":
    run(main())
