import re

from prompt_toolkit import PromptSession, validation
from prompt_toolkit.application import get_app
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style

rx_expr = re.compile(r"^(\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\d+(?:\.\d+)?)$")
rx_leading_zero = re.compile(r"^0\d.*$")


class ExpressionValidator(validation.Validator):
    def validate(self, document):
        expression = document.text
        if not rx_expr.match(expression):
            self.raise_(expression)
        match = rx_expr.findall(expression)
        if len(match) != 1:
            self.raise_(expression)
        groups = match[0]
        if len(groups) != 3:
            self.raise_(expression)
        if groups[1] == "/" and groups[2] == "0":
            self.raise_(expression)
        if rx_leading_zero.match(groups[0]) or rx_leading_zero.match(groups[2]):
            self.raise_(expression)

    @staticmethod
    def raise_(expression: str):
        raise validation.ValidationError(
            message=f"invalid expression '{expression}'",
            cursor_position=len(expression),
        )


def bottom_toolbar():
    if not (app := get_app()):
        return
    hist_len = len(app.current_buffer.history.get_strings())
    return [("class:bottom-toolbar", f" history size: {hist_len} ")]


if __name__ == "__main__":
    session = PromptSession(
        "> ",
        auto_suggest=AutoSuggestFromHistory(),
        bottom_toolbar=bottom_toolbar,
        validator=ExpressionValidator(),
        validate_while_typing=False,
        style=Style.from_dict({"bottom-toolbar": "#333333 bg:#e0df0c"}),
        vi_mode=True,
    )
    try:
        while input_text := session.prompt():
            print(eval(input_text))
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as e:
        print(repr(e))
