from typing import Dict
from urllib.request import urlopen

from utils import *


def get_results() -> Dict[int, int] | None:
    if raw_results := make_req(RESULTS_URL, timeout=300):
        return parse_results(raw_results)


def make_req(url: str, timeout=1000) -> str | None:
    try:
        with urlopen(url, timeout=timeout) as resp:
            log.info(f"GET {resp.status} {resp.msg} {url}")
            if resp.status == 200:
                return resp.read().decode().strip()
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
