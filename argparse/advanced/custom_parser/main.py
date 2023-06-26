import argparse
from dataclasses import dataclass
import sys
from textwrap import dedent
from typing import IO, List, Optional


ASCII_ART = r"""                __    __                         
               /\ \__/\ \                        
 _____   __  __\ \ ,_\ \ \___     ___     ___    
/\ '__`\/\ \/\ \\ \ \/\ \  _ `\  / __`\ /' _ `\  
\ \ \L\ \ \ \_\ \\ \ \_\ \ \ \ \/\ \L\ \/\ \/\ \ 
 \ \ ,__/\/`____ \\ \__\\ \_\ \_\ \____/\ \_\ \_\
  \ \ \/  `/___/> \\/__/ \/_/\/_/\/___/  \/_/\/_/
   \ \_\     /\___/                              
    \/_/     \/__/

"""
MULTILINE_HELP_TEXT = """
enviroment variables:
    FOO: to provide `foo`
    BAR: to provide `bar`
"""


class MainArgType:
    def __init__(self, value: str) -> None:
        self._validate(value)
        self.value = value

    def __repr__(self) -> str:
        return "%s(value='%s')" % (self.__class__.__name__, self.value)

    def _validate(self, value: str) -> None:
        if not value:
            raise argparse.ArgumentTypeError("invalid main argument")


@dataclass
class ArgsModel:
    main: MainArgType
    optional: Optional[str] = None


class MyArgsParser(argparse.ArgumentParser):
    def __init__(self, **kwargs) -> None:
        self.additional_help_text = kwargs.pop("additional_help_text", "")
        self.ascii_art = kwargs.pop("ascii_art", "")
        super().__init__(**kwargs)

    def parse_args(self, args: Optional[List[str]] = None) -> ArgsModel:
        return ArgsModel(**vars(super().parse_args(args)))

    def print_help(self, file: Optional[IO[str]] = None) -> None:
        file = file or sys.stdout
        file.write(self.ascii_art)
        super().print_help(file)
        file.write(self.additional_help_text)


def parse_args(test_args: Optional[List[str]] = None) -> ArgsModel:
    parser = MyArgsParser(
        prog="progname",
        usage="%(prog)s MAIN_ARG [-o VALUE]",
        ascii_art=ASCII_ART,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        additional_help_text=dedent(MULTILINE_HELP_TEXT),
        epilog="Text at the bottom of help and above the additional_help_text",
        exit_on_error=False,
    )
    parser.add_argument("main", type=MainArgType, help="main argument")
    parser.add_argument("-o", "--optional", help="optional argument")
    return parser.parse_args(test_args)


if __name__ == "__main__":
    if sys.argv[1:]:
        print(parse_args())
    else:
        print(parse_args("first --opt test".split()))
        print(parse_args("-o test second".split()))
        print(parse_args(["third"]))
