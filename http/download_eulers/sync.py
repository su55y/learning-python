from html.parser import HTMLParser

# from logging import info, error, basicConfig, INFO
import logging
from pathlib import Path
from re import match
from textwrap import wrap
from typing import Dict, Tuple
from urllib.request import urlopen

PROJECT_EULER_URL = "https://projecteuler.net/minimal=%d"
RESULTS_URL = "https://raw.githubusercontent.com/zengin/project-euler-solutions/master/results.txt"

PROBLEMS_DIR_NAME = "problems"
LOG_FMT = "[\x1b[38;5;44m%(asctime)s %(levelname)s\x1b[0m] %(message)s"


def init_logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(LOG_FMT, "%H:%M:%S %d/%m/%y"))
    log.addHandler(sh)
    return log


log = init_logger()


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
    if raw_results := make_req(RESULTS_URL, timeout=300):
        return parse_results(raw_results)


def init_dir() -> Path | None:
    dir_path = Path(PROBLEMS_DIR_NAME)
    try:
        if not dir_path.exists():
            dir_path.mkdir()
    except:
        log.error(f"can't make dir by path {dir_path.absolute()}")
    else:
        return dir_path.absolute()


def make_req(url: str, timeout=1000) -> str | None:
    try:
        with urlopen(url, timeout=timeout) as resp:
            log.info(f"GET {resp.status} {resp.msg} {url}")
            if resp.status == 200:
                return resp.read().decode().strip()
    except Exception as e:
        log.error(repr(e))


def write_problem(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
    except Exception as e:
        log.error(repr(e))


def main():
    if not (dir_path := init_dir()):
        exit(1)
    euler_parser = EulerMinimalParser()
    results = get_results() or {}

    for i in range(1, 51):
        if not (raw_problem := make_req(PROJECT_EULER_URL % i)):
            continue
        euler_parser.feed(raw_problem)
        result_value = results.get(i)
        result = "" if not result_value else f"\nexpected result: {result_value}\n"
        write_problem(
            dir_path.joinpath(f"problem{i}.txt"),
            f"Problem #{i}\n{euler_parser.get_problem()}\n{result}",
        )


if __name__ == "__main__":
    main()
