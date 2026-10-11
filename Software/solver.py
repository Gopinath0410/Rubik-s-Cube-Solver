import kociemba
from tkinter import messagebox


class CubeSolver:

    @staticmethod
    def validate(cube_state):

        for face in cube_state.faces.values():

            if "gray40" in face:

                messagebox.showerror(
                    "Incomplete Cube",
                    "Please fill all stickers before solving."
                )

                return False

        return True

    @staticmethod
    def solve(cube_string):

        try:
            print("Length:", len(cube_string))
            print("repr :", repr(cube_string))
            print("cube :", cube_string)

            solution = kociemba.solve(cube_string)

            return solution

        except Exception as e:

            messagebox.showerror(
                "Invalid Cube",
                repr(e)
            )

            return None