from argparse import ArgumentParser
import argparse
import sys
from textwrap import dedent
from typing import IO, Type

ADDITIONAL_HELP_TEXT = """
enviroment variables:
    FOO: to provide `foo`
    BAR: to provide `bar`
"""


class MyArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs) -> None:
        self.additional_help_text = kwargs.pop("additional_help_text", "")
        super().__init__(*args, **kwargs)
        self.add_argument(
            "argument",
            type=MainArgumentType.validate,
            help="the main argument",
        )
        self.args = self.parse_args()
        self.argument: MainArgumentType = self.args.argument

    def print_help(self, file: IO[str] | None = None) -> None:
        super().print_help(file)
        if self.additional_help_text:
            if not file:
                file = sys.stdout
            file.write(self.additional_help_text)


class MainArgumentType:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"

    @classmethod
    def validate(cls: Type["MainArgumentType"], arg: str) -> "MainArgumentType":
        if not arg:
            raise argparse.ArgumentTypeError("invalid main argument")
        return cls(arg)


def parse_args() -> MyArgumentParser:
    return MyArgumentParser(additional_help_text=dedent(ADDITIONAL_HELP_TEXT))


if __name__ == "__main__":
    args = parse_args()
    print(args.argument)
