import customtkinter as ctk

COLORS = [
    ("White", "white"),
    ("Yellow", "yellow"),
    ("Green", "green"),
    ("Blue", "blue"),
    ("Red", "red"),
    ("Orange", "orange")
]

current_popup = None


def close_popup():
    global current_popup

    if current_popup is not None:
        current_popup.destroy()
        current_popup = None


def show_picker(app, button, callback):

    global current_popup

    close_popup()

    popup = ctk.CTkToplevel(app)
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)

    current_popup = popup

    x = button.winfo_rootx()
    y = button.winfo_rooty() + button.winfo_height() + 5

    popup.geometry(f"+{x}+{y}")

    frame = ctk.CTkFrame(popup)
    frame.pack(padx=5, pady=5)

    row = 0
    col = 0

    for _, color in COLORS:

        def choose(c=color):
            callback(button, c)
            close_popup()

        b = ctk.CTkButton(
            frame,
            text="",
            width=42,
            height=42,
            fg_color=color,
            hover_color=color,
            command=choose
        )

        b.grid(
            row=row,
            column=col,
            padx=3,
            pady=3
        )

        col += 1

        if col == 3:
            col = 0
            row += 1