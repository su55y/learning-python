from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int

    def __setattr__(self, key, val):
        if key == "age" and val <= 0:
            raise ValueError(
                f"invalid {key!r} value {val!r}, should be greater then zero"
            )
        self.__dict__[key] = val
