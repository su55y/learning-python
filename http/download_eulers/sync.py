from urllib.request import urlopen

from utils import log, ProblemsHandler, PROJECT_EULER_URL, RESULTS_URL


def fetch(url: str, timeout=1000) -> str:
    try:
        with urlopen(url, timeout=timeout) as resp:
            log.info(f"GET {resp.status} {resp.msg} {url}")
            if resp.status != 200:
                raise Exception(f"response status {resp.status}")
            return resp.read().decode().strip()
    except Exception as e:
        log.error("can't fetch results: %s" % e)
        return ""


def main():
    results = fetch(RESULTS_URL)
    problems = [p for i in range(1, 51) if (p := fetch(PROJECT_EULER_URL % i))]
    h = ProblemsHandler(raw_problems=problems, raw_results=results)
    h.write_problems()


if __name__ == "__main__":
    main()
