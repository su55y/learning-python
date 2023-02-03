from html.parser import HTMLParser
from logging import info, error, basicConfig, INFO
from os import path, mkdir
from re import match
from textwrap import wrap
from typing import Dict, List, Tuple
from urllib.request import urlopen

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


def get_results() -> Dict[int, int] | None:
    raw_results, ok = make_req(RESULTS_URL, timeout=300)
    if not ok:
        return None
    return parse_results(raw_results)


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


def make_req(URL, timeout=1000) -> Tuple[str, bool]:
    try:
        with urlopen(URL, timeout=timeout) as resp:
            info(f"GET {resp.status} {resp.msg} {URL}")
            if resp.status == 200:
                return resp.read().decode().strip(), True
    except Exception as e:
        error(repr(e))

    return "", False


def main():
    basicConfig(
        level=INFO,
        format="\x1b[38;5;44m%(asctime)s [%(levelname)s]:\x1b[0m %(message)s",
        datefmt="%H:%M:%S %d/%m/%y",
    )
    if not init_dir():
        exit(1)
    results = get_results()
    euler_parser = EulerMinimalParser()
    problems_list: List[Tuple[int, str, int | None]] = list()

    for i in range(1, 51):
        raw_problem, ok = make_req(PROJECT_EULER_URL % i)
        if not ok:
            continue

        euler_parser.feed(raw_problem)
        result = None
        if results and i in results.keys():
            result = results.get(i)

        problems_list.append((i, euler_parser.get_problem(), result))

    for (index, text, result) in problems_list:
        try:
            with open(f"{PROBLEMS_DIR_NAME}/problem{index}", "w") as file:
                result = "" if not result else f"\nexpected result: {result}\n"
                file.write(f"Problem #{index}\n{text}\n{result}")
        except Exception as e:
            error(repr(e))


if __name__ == "__main__":
    main()
