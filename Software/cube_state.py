class CubeState:

    def __init__(self):

        self.color_count = {
            "white": 1,
            "yellow": 1,
            "green": 1,
            "blue": 1,
            "red": 1,
            "orange": 1
        }

        self.faces = {
            "U": ["gray40"] * 9,
            "R": ["gray40"] * 9,
            "F": ["gray40"] * 9,
            "D": ["gray40"] * 9,
            "L": ["gray40"] * 9,
            "B": ["gray40"] * 9
        }

        # Fixed centre colours
        self.faces["U"][4] = "white"
        self.faces["R"][4] = "red"
        self.faces["F"][4] = "green"
        self.faces["D"][4] = "yellow"
        self.faces["L"][4] = "orange"
        self.faces["B"][4] = "blue"

    def change_color(self, old_color, new_color):

        if old_color == new_color:
            return True, ""

        if new_color != "gray40":

            if self.color_count[new_color] >= 9:
                return False, f"{new_color.capitalize()} already has 9 stickers."

            self.color_count[new_color] += 1

        if old_color != "gray40":
            self.color_count[old_color] -= 1

        return True, ""

    def to_solver_string(self):

        colour_map = {
            "white": "U",
            "red": "R",
            "green": "F",
            "yellow": "D",
            "orange": "L",
            "blue": "B"
        }

        cube = ""

        # IMPORTANT ORDER
        for face in ["U", "R", "F", "D", "L", "B"]:

            for colour in self.faces[face]:
                cube += colour_map[colour]

        return cube