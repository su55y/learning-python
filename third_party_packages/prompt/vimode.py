from prompt_toolkit import prompt
from prompt_toolkit.application.current import get_app
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.key_binding.vi_state import InputMode
from prompt_toolkit.styles import Style

C_TOOLBAR_INSERT = "toolbar_insert"
C_TOOLBAR_VI = "toolbar_vi"
styles = {C_TOOLBAR_INSERT: "#2c2829 bg:#83a598", C_TOOLBAR_VI: "#2c2829 bg:#a89984"}


def bottom_toolbar():
    if not (app := get_app()):
        return
    match app.vi_state.input_mode:
        case InputMode.INSERT:
            mode = "INSERT"
            classname = C_TOOLBAR_INSERT
            app.output.set_cursor_shape(cursor_shape=CursorShape.BEAM)
        case _:
            mode = "NORMAL"
            classname = C_TOOLBAR_VI
            app.output.set_cursor_shape(cursor_shape=CursorShape.BLOCK)
    return [(f"class:{classname}", f" [{mode}] ")]


def use_prompt() -> str:
    return prompt(
        "> ",
        vi_mode=True,
        bottom_toolbar=bottom_toolbar,
        style=Style.from_dict(styles),
    )


if __name__ == "__main__":
    try:
        while text := use_prompt():
            print(text)
    except:
        pass
