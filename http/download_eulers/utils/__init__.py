from html.parser import HTMLParser
import logging
from pathlib import Path
import re
from textwrap import wrap
from typing import Dict, List


PROJECT_EULER_URL = "https://projecteuler.net/minimal=%d"
RESULTS_URL = "https://raw.githubusercontent.com/zengin/project-euler-solutions/master/results.txt"

PROBLEMS_PATH = "problems"
LOG_FMT = "[\x1b[38;5;44m%(asctime)s %(levelname)s\x1b[0m] %(message)s"


def init_logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(LOG_FMT, "%H:%M:%S %d/%m/%y"))
    log.addHandler(sh)
    return log


log = init_logger()

__all__ = [
    "log",
    "ProblemsHandler",
    "PROJECT_EULER_URL",
    "RESULTS_URL",
]


def init_dir() -> Path:
    path = Path(PROBLEMS_PATH)
    try:
        if not path.exists():
            path.mkdir()
        return path
    except Exception as e:
        logging.error("can't mkdir %s: %s" % (path, e))
        exit(1)


class EulerMinimalParser(HTMLParser):
    _problem = ""

    @property
    def problem(self) -> str:
        problem_text = "".join([s.strip() for s in self._problem.splitlines(True)])
        problem_text = "\n".join(wrap(problem_text, 80, break_long_words=False)).strip()
        self._problem = ""
        return problem_text

    def handle_data(self, data):
        self._problem += f"{data}\n"


class ProblemsHandler:
    def __init__(self, raw_problems: List[str], raw_results: str) -> None:
        self.path = init_dir()
        self.results = self._parse_results(raw_results)
        self.problems = self._parse_problems(raw_problems)
        self.write_problems()

    def write_problems(self):
        for i, p in enumerate(self.problems):
            try:
                with open(self.path.joinpath("problem%d.txt" % (i + 1)), "w") as file:
                    file.write(p)
            except Exception as e:
                logging.error("can't write problem: %s" % e)

    def _parse_problems(self, raw_problems: List[str]) -> List[str]:
        problems = []
        for i, p in enumerate(raw_problems):
            parser = EulerMinimalParser()
            parser.feed(p)
            result = "" if (r := self.results.get(i + 1)) is None else "%d\n" % r
            problems.append(f"Problem #{i+1}\n{parser.problem}\n{result}")
        return problems

    def _parse_results(self, raw_results: str) -> Dict[int, int]:
        results: Dict[int, int] = {}
        rx_result = re.compile(r"^0\d{2}\:\s-?\d+$")
        for line in raw_results.split():
            if not rx_result.match(line):
                continue
            index, result = line.replace(":", "").split()
            results[int(index, 10)] = int(result, 10)

        return results
