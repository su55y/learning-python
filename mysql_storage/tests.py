from collections.abc import Callable
from typing import Dict
from country import CountriesStorage, Country, List
from time import perf_counter
from datetime import datetime

stor = CountriesStorage()
log = lambda *args: print(datetime.utcnow().strftime('%H:%M:%S.%f')[:-3], *args)


def select_one_test():
    ukraine, err = stor.select_one(where="capital = 'Kyiv'")
    assert err is None, f"err should be None: {repr(err)}"
    assert isinstance(ukraine, Country), "ukraine should be instance of Country"
    assert ukraine.country == "Ukraine", "country attribute should by 'Ukraine'"
    assert ukraine.capital == "Kyiv", "capital attribute should by 'Kyiv'"

def select_one_not_found_test():
    raj, err = stor.select_one(where="capital = 'Dehli'")
    assert isinstance(err, IndexError), f"err should be IndexError: {repr(err)}"
    assert raj is None, "raj should be None"

def select_all_test():
    countries, err = stor.select()
    assert err is None, f"err should be None: {repr(err)}"
    assert isinstance(countries, List),\
        f"countries should be list ({type(countries).__name__})"
    assert len(countries) == 3, f"countries length != 3 (len: {len(countries)})"
    assert isinstance(countries[0], Country),\
        f"countries item should be instance of Country ({type(countries[0]).__name__})"

def select_where_test():
    countries, err = stor.select(where="capital != 'Kyiv'")
    assert err is None, f"err should be None: {repr(err)}"
    assert len(countries) == 2, f"countries length != 2 (len: {len(countries)})"
    assert Country(0, "Poland", "Warsaw") in countries and\
        Country(0, "United Kingdom", "London") in countries,\
        f"Poland and UK should be in countries: {countries}"

def equality_test():
    poland = Country(0, "Poland", "Warsaw")
    assert isinstance(poland, Country), "poland should be instance of Country"
    assert poland == Country(id=0, country="Poland", capital="Warsaw"),\
        "poland should be equal Country('Poland', 'Warsaw')"

def insert_test():
    pass


def run_tests(tests_dict: Dict[str, Dict[str, Callable]]):
    for section, tests in tests_dict.items():
        section_passed = True
        log(f"[START] {section}:")
        for name, test in tests.items():
            try:
                test()
            except Exception as e:
                log(f"-- [FAIL] {name} NOT passed: {e}")
                section_passed = False
            else:
                log(f"-- [OK] {name} passed")

        log(" ".join(f"""[{'FAIL' if not section_passed else 'OK'}]\
                {section}: {'NOT ' if not section_passed else ''}\
                PASSED""".split()))
        print()

        

def main():
     run_tests({
        "coutry storage tests": {
            "select_one_test": select_one_test,
            "select_one_not_found_test": select_one_not_found_test,
            "select_all_test": select_all_test,
            "select_where_test": select_where_test,
        },
        "coutry dataclass tests": {
            "equality_test": equality_test,
        },
    })

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print(f"\n-- all tests done in {(end - start)*1000:.0f}ms")
