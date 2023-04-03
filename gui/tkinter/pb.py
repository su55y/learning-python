from time import sleep

from tkinter import Tk, Button, Label, Frame, StringVar
from tkinter.ttk import Progressbar


def with_hide(callback):
    def wrapper(*args, **kwargs):
        global start_button
        start_button.pack_forget()
        callback(*args, **kwargs)
        start_button.pack()

    return wrapper


@with_hide
def start():
    global progress_bar, percent, window
    match progress_bar["value"]:
        case 101:
            direction = -1
            condition = lambda v: v >= 0
        case _:
            direction = 1
            condition = lambda v: v <= 100

    while condition(progress_bar["value"]):
        percent.set(f"{progress_bar['value']}%")
        progress_bar["value"] += direction
        window.update_idletasks()
        sleep(0.01)


if __name__ == "__main__":
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
