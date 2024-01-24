from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout.containers import Window, VSplit, WindowAlign
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout

kb = KeyBindings()


@kb.add("c-c")
def exit_(event: KeyPressEvent):
    event.app.exit()


@kb.add("c-l")
def clean_(event: KeyPressEvent):
    event.app.current_buffer.text = ""


def on_text_changed_handler(buf1: Buffer, buf2: Buffer):
    buf2.text = buf1.text[::-1]


if __name__ == "__main__":
    buf1 = Buffer()
    buf2 = Buffer()

    buf1.on_text_changed += lambda buf: on_text_changed_handler(buf, buf2)

    win1 = Window(BufferControl(buf1))
    win2 = Window(BufferControl(buf2), align=WindowAlign.RIGHT)
    layout = Layout(VSplit([win1, Window(width=1, char="|"), win2]))

    app = Application(layout=layout, key_bindings=kb)
    app.run()
