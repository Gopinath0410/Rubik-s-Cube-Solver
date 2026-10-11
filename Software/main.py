import customtkinter as ctk
from cube_face import CubeFace
from cube_state import CubeState
from solver import CubeSolver
from serial_manager import SerialManager

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ==========================================================
# APP
# ==========================================================

app = ctk.CTk()
app.title("Rubik Cube Solver")
app.geometry("1450x900")

cube_state = CubeState()
serial_manager = SerialManager()

# ==========================================================
# TITLE
# ==========================================================

title = ctk.CTkLabel(
    app,
    text="Rubik Cube Solver",
    font=("Arial", 30, "bold")
)

title.grid(
    row=0,
    column=0,
    columnspan=2,
    pady=20
)

# ==========================================================
# LEFT SIDE (Cube Faces)
# ==========================================================

layout = ctk.CTkFrame(app)
layout.grid(
    row=1,
    column=0,
    padx=20,
    pady=20,
    sticky="n"
)

CubeFace(layout, app, cube_state, "U").grid(
    row=0,
    column=0,
    pady=15
)

CubeFace(layout, app, cube_state, "L").grid(
    row=1,
    column=0,
    padx=10
)

CubeFace(layout, app, cube_state, "F").grid(
    row=1,
    column=1,
    padx=10
)

CubeFace(layout, app, cube_state, "R").grid(
    row=1,
    column=2,
    padx=10
)

CubeFace(layout, app, cube_state, "B").grid(
    row=0,
    column=2,
    padx=10
)

CubeFace(layout, app, cube_state, "D").grid(
    row=0,
    column=1,
    pady=15
)

# ==========================================================
# RIGHT SIDE PANEL
# ==========================================================

side_frame = ctk.CTkFrame(app, width=300)
side_frame.grid(
    row=1,
    column=1,
    sticky="ns",
    padx=20,
    pady=20
)

# ==========================================================
# SERIAL SECTION
# ==========================================================

serial_title = ctk.CTkLabel(
    side_frame,
    text="Serial Connection",
    font=("Arial", 18, "bold")
)

serial_title.pack(pady=(10,10))

ports = serial_manager.get_ports()

if not ports:
    ports = ["No Ports"]

port_menu = ctk.CTkOptionMenu(
    side_frame,
    values=ports,
    width=220
)

port_menu.pack(pady=5)

status = ctk.CTkLabel(
    side_frame,
    text="Disconnected",
    text_color="red"
)

status.pack(pady=10)


def connect_serial():

    port = port_menu.get()

    if port == "No Ports":
        return

    if serial_manager.connect(port):

        status.configure(
            text=f"Connected ({port})",
            text_color="green"
        )


def refresh_ports():

    ports = serial_manager.get_ports()

    if not ports:
        ports = ["No Ports"]

    port_menu.configure(values=ports)
    port_menu.set(ports[0])


connect_btn = ctk.CTkButton(
    side_frame,
    text="Connect",
    width=220,
    command=connect_serial
)

connect_btn.pack(pady=5)

refresh_btn = ctk.CTkButton(
    side_frame,
    text="Refresh Ports",
    width=220,
    command=refresh_ports
)

refresh_btn.pack(pady=5)

ctk.CTkLabel(
    side_frame,
    text="Solution",
    font=("Arial", 18, "bold")
).pack(pady=(10, 10))

move_count_label = ctk.CTkLabel(
    side_frame,
    text="Moves: 0",
    font=("Arial", 16, "bold")
)

move_count_label.pack(pady=5)

solution_box = ctk.CTkTextbox(
    side_frame,
    width=260,
    height=30,
    font=("Consolas", 15)
)

solution_box.pack(padx=10, pady=10)

# ==========================================================
# SOLVER
# ==========================================================


def solve_cube():

    if not CubeSolver.validate(cube_state):
        return

    cube_string = cube_state.to_solver_string()

    print("Cube String:")
    print(cube_string)

    solution = CubeSolver.solve(cube_string)

    if solution:

            moves = solution.split()

    move_count_label.configure(
        text=f"Moves: {len(moves)}"
    )

    solution_box.delete("1.0", "end")

    solution_box.insert(
        "end",
        " ".join(moves)
    )

    print("Solution:")
    print(solution)

    serial_manager.send_moves(solution)



# ==========================================================
# DEBUG
# ==========================================================

def print_cube():

    print(cube_state.faces)


# ==========================================================
# RESET
# ==========================================================

def reset_cube():

    for face_widget in layout.winfo_children():

        if isinstance(face_widget, CubeFace):

            for row in face_widget.buttons:

                for button in row:

                    if button.index == 4:
                        continue

                    button.configure(
                        fg_color="gray40",
                        hover_color="gray40"
                    )

            face = face_widget.face

            cube_state.faces[face] = ["gray40"] * 9
            cube_state.faces[face][4] = face_widget.default_color

    cube_state.color_count = {
        "white": 1,
        "yellow": 1,
        "green": 1,
        "blue": 1,
        "red": 1,
        "orange": 1
    }

    print("Cube Reset")


# ==========================================================
# BUTTONS
# ==========================================================

button_title = ctk.CTkLabel(
    side_frame,
    text="Controls",
    font=("Arial",18,"bold")
)

button_title.pack(pady=(10,10))

solve_button = ctk.CTkButton(
    side_frame,
    text="Solve Cube",
    width=220,
    height=40,
    command=solve_cube
)

solve_button.pack(pady=6)

reset_button = ctk.CTkButton(
    side_frame,
    text="Reset Cube",
    width=220,
    height=40,
    command=reset_cube
)

reset_button.pack(pady=6)

debug_btn = ctk.CTkButton(
    side_frame,
    text="Print Cube",
    width=220,
    height=40,
    command=print_cube
)

debug_btn.pack(pady=6)

app.mainloop()