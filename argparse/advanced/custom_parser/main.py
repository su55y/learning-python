from argparse import ArgumentParser, ArgumentTypeError, RawDescriptionHelpFormatter
from dataclasses import dataclass
import sys
from textwrap import dedent
from typing import IO, Optional

MULTILINE_HELP_TEXT = """
enviroment variables:
    FOO: to provide `foo`
    BAR: to provide `bar`
"""


class MainArgType:
    def __init__(self, value: str) -> None:
        self._validate(value)
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"

    def _validate(self, value: str) -> None:
        if not value:
            raise ArgumentTypeError("invalid main argument")


@dataclass
class ArgsModel:
    main: MainArgType
    optional: int


class MyArgsParser(ArgumentParser):
    def __init__(self, *args, **kwargs) -> None:
        self.additional_help_text = kwargs.pop("additional_help_text", "")
        super().__init__(*args, **kwargs)

    @property
    def args(self) -> ArgsModel:
        return ArgsModel(**vars(super().parse_args()))

    def print_help(self, file: Optional[IO[str]] = None) -> None:
        super().print_help(file)
        if self.additional_help_text:
            if not file:
                file = sys.stdout
            file.write(self.additional_help_text)


def ascii_art() -> Optional[str]:
    try:
        with open("ascii_art.txt") as f:
            return f.read()
    except:
        pass


def parse_args() -> ArgsModel:
    parser = MyArgsParser(
        prog="progname",
        description=ascii_art() or "",
        formatter_class=RawDescriptionHelpFormatter,
        additional_help_text=dedent(MULTILINE_HELP_TEXT),
    )
    parser.add_argument(
        "main",
        type=MainArgType,
        help="main argument",
    )
    parser.add_argument("--optional", type=int, help="optional argument")
    return parser.args


if __name__ == "__main__":
    print(parse_args())
