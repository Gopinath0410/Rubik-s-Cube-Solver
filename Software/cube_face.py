import customtkinter as ctk
from tkinter import messagebox
from color_picker import show_picker
EMPTY_COLOR = "gray40"
FACE_COLORS = {
    "U": "white",
    "L": "orange",
    "F": "green",
    "R": "red",
    "B": "blue",
    "D": "yellow"
}


class CubeFace(ctk.CTkFrame):

    def __init__(self, master, app, cube_state, face_name):

        super().__init__(master)

        self.app = app
        self.cube_state = cube_state
        self.face = face_name
        self.default_color = FACE_COLORS[face_name]

        self.buttons = []

        title = ctk.CTkLabel(
            self,
            text=face_name,
            font=("Arial", 18, "bold")
        )

        title.pack(pady=(8, 5))

        grid = ctk.CTkFrame(self)
        grid.pack(padx=8, pady=8)

        for r in range(3):

            row = []

            for c in range(3):
                index = r * 3 + c

                if r == 1 and c == 1:
                    colour = self.default_color
                else:
                    colour = EMPTY_COLOR

                button = ctk.CTkButton(
                    grid,
                    text="",
                    width=60,
                    height=60,
                    fg_color=colour,
                    hover_color=colour
                )
                button.index = index
                button.grid(
                    row=r,
                    column=c,
                    padx=4,
                    pady=4
                )

                # Lock the centre sticker
                if r == 1 and c == 1:

                    button.configure(state="disabled")

                else:

                    button.configure(
                        command=lambda b=button: show_picker(
                            self.app,
                            b,
                            self.change_sticker_color
                        )
                    )

                row.append(button)

            self.buttons.append(row)

    # -------------------------------------------------------
    # Change Sticker Colour
    # -------------------------------------------------------

    def change_sticker_color(self, button, new_color):

        old_color = button.cget("fg_color")

        if isinstance(old_color, tuple):
            old_color = old_color[0]

        success, message = self.cube_state.change_color(
            old_color,
            new_color
        )

        if not success:
            messagebox.showerror(
                "Invalid Colour",
                message
            )
            return

        button.configure(
            fg_color=new_color,
            hover_color=new_color
            
        )
        index = button.index
        self.cube_state.faces[self.face][index] = new_color