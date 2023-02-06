from collections.abc import Callable
from tkinter import Tk, Button, Label, Frame, StringVar
from tkinter.ttk import Progressbar
from time import sleep
from typing import Any


def with_hide(callback: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        global start_button
        start_button.pack_forget()
        callback(*args, **kwargs)
        start_button.pack()

    return wrapper


@with_hide
def start():
    global progress_bar, percent, window
    progress_bar.configure(value=0)

    while progress_bar["value"] <= 100:
        percent.set(f"{progress_bar['value']}%")
        progress_bar["value"] += 1
        window.update_idletasks()
        sleep(0.01)


window = Tk()
frame = Frame(window, padx=25, pady=25)
frame.pack()

progress_bar = Progressbar(frame, length=300, value=0)
progress_bar.pack(pady=10)

percent = StringVar()
percent_label = Label(frame, textvariable=percent).pack()

start_button = Button(frame, text="start", command=start)
start_button.pack()

window.mainloop()
