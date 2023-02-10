from collections.abc import Callable
from typing import Dict, List

from country import CountriesStorage, Country
from time import perf_counter
from datetime import datetime
from sys import argv

stor = CountriesStorage()
t = stor.tb_countries

log = lambda *args: print(datetime.utcnow().strftime("%H:%M:%S.%f")[:-3], *args)
verbose = "-v" in argv[1:]


def select_one_test():
    ukraine, err = stor.select_one(where=(t.capital == "Kyiv"))
    assert err is None, f"select error: {repr(err)}"
    assert isinstance(ukraine, Country), "ukraine should be instance of Country"
    assert ukraine.country == "Ukraine", "country attribute should by 'Ukraine'"
    assert ukraine.capital == "Kyiv", "capital attribute should by 'Kyiv'"


def select_one_not_found_test():
    raj, err = stor.select_one(where=(t.capital == "Dehli"))
    assert isinstance(err, IndexError), f"err should be IndexError: {repr(err)}"
    assert raj is None, "raj should be None"


def select_all_test():
    countries, err = stor.select()
    assert err is None, f"select error: {repr(err)}"
    assert isinstance(
        countries, List
    ), f"countries should be list ({type(countries).__name__})"
    assert len(countries) == 3, f"countries length != 3 (len: {len(countries)})"
    assert isinstance(
        countries[0], Country
    ), f"countries item should be instance of Country ({type(countries[0]).__name__})"


def select_where_test():
    countries, err = stor.select(where=(t.capital != "Kyiv"), limit=1)
    assert err is None, f"select error: {repr(err)}"
    assert len(countries) == 1, f"countries length != 1 (len: {len(countries)})"
    assert (
        Country(None, "Poland", "Warsaw") in countries
        or Country(None, "United Kingdom", "London") in countries
    ), f"Poland or UK should be in countries: {countries}"


def insert_test():
    count, err = stor.insert([Country(id=None, country="Raj", capital="Delhi")])
    assert err is None, f"insert error: {repr(err)}"
    assert count == 1, f"inserted rows count != 1"


def update_test():
    india = Country(None, "India", "New-Delhi")
    count, err = stor.update([india], where=(t.country == "Raj"))
    assert err is None, f"update error: {repr(err)}"
    assert count == 1, f"updated rows != 1 ({count})"
    updated_india, sel_err = stor.select_one(where=(t.capital == "New-Delhi"))
    assert sel_err is None, f"select error: {repr(err)}"
    assert (
        Country(None, "India", "New-Delhi") == updated_india
    ), f"unexpected india: {india}, capital should be 'New-Delhi'"


def delete_test():
    india, err = stor.select_one(where=(t.country == "India"))
    assert err is None, f"select error: {repr(err)}"
    assert isinstance(india, Country), f"india should be coutry"
    count, err = stor.delete(where=(t.id == india.id))
    assert err is None, f"delete error: {repr(err)}"
    assert count == 1, f"deleted rows != 1 ({count})"


def equality_test():
    poland = Country(None, "Poland", "Warsaw")
    assert isinstance(poland, Country), "poland should be instance of Country"
    assert poland == Country(
        id=0, country="Poland", capital="Warsaw"
    ), "poland should be equal Country('Poland', 'Warsaw')"


def run_tests(tests_dict: Dict[str, Dict[str, Callable]]):
    for section, tests in tests_dict.items():
        section_passed = True
        if verbose:
            log(f"[START] {section}:")
        for name, test in tests.items():
            try:
                test()
            except Exception as e:
                log(f"-- [FAIL] {name} NOT passed: {e}")
                section_passed = False
            else:
                if verbose:
                    log(f"-- [OK] {name} passed")

        log(
            " ".join(
                f"""[{'FAIL' if not section_passed else 'OK'}]\
                {section}: {'NOT ' if not section_passed else ''}\
                PASSED""".split()
            ),
            "\n" if verbose else "",
        )


def main():
    run_tests(
        {
            "country storage tests": {
                "select_one_test": select_one_test,
                "select_one_not_found_test": select_one_not_found_test,
                "select_all_test": select_all_test,
                "select_where_test": select_where_test,
                "insert_test": insert_test,
                "update_test": update_test,
                "delete_test": delete_test,
            },
            "coutry dataclass tests": {
                "equality_test": equality_test,
            },
        }
    )


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print(f"\n-- all tests done in {(end - start)*1000:.0f}ms")
