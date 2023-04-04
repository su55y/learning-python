import itertools as itr

import tkinter as tk


BOARD_LENGTH = 8  # !! max_scale == (screen_height/2)*BOARD_LENGTH


class ScalableFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, height: float, **kwargs):
        tk.Frame.__init__(self, parent, height=height, **kwargs)
        self.bind_all("<Button-4>", self.zoom)
        self.bind_all("<Button-5>", self.zoom)
        self.max_scale = height * BOARD_LENGTH
        self.min_scale = height / BOARD_LENGTH
        self.canvas_size = height

    def zoom(self, event: tk.Event):
        match event.num:
            case 4:
                self.scale = 2
            case 5:
                self.scale = 0.5
            case _:
                return
        if (
            self.max_scale <= self.scale * self.canvas_size
            or self.min_scale >= self.scale * self.canvas_size
        ):
            return
        if child := self.winfo_children().pop():
            if isinstance(child, tk.Canvas):
                self.canvas_size = child.winfo_height() * self.scale

                child.scale("all", 0, 0, self.scale, self.scale)
                child.place(
                    relx=0.5,
                    rely=0.5,
                    width=self.canvas_size,
                    height=self.canvas_size,
                )


def chessboard_canvas(parent: ScalableFrame, **kwargs):
    canvas = tk.Canvas(parent, **kwargs)
    if height := kwargs.get("height"):
        rect_size = height / BOARD_LENGTH

        for i, (x, y) in enumerate(
            itr.product(
                itr.takewhile(lambda n: n < height, itr.count(step=rect_size)), repeat=2
            )
        ):
            canvas.create_rectangle(
                x,
                y,
                x + rect_size,
                y + rect_size,
                fill=["#000", "#fff"][(i // BOARD_LENGTH + i % BOARD_LENGTH) % 2 == 0],
                width=0,
            )
    return canvas


if __name__ == "__main__":
    window = tk.Tk(className="floating")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_size = int(screen_height * 0.5)
    window_x = int((screen_width - window_size) / 2)
    window_y = int((screen_height - window_size) / 2)
    window.geometry(f"{window_size}x{window_size}+{window_x}+{window_y}")

    frame = ScalableFrame(
        window,
        width=window_size,
        height=window_size,
        highlightthickness=0,
    )
    frame.pack(expand=True)

    chessboard_canvas(
        frame,
        width=window_size,
        height=window_size,
        borderwidth=0,
        highlightthickness=0,
    ).place(relx=0.5, rely=0.5, anchor="center")

    exit(window.mainloop())
