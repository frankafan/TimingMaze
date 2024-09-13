from timing_maze_game import TimingMazeGame
import tkinter as tk


# Namespace class to store the arguments
class Namespace:
    def __init__(self, **kwargs):
        # Initialize the class with the given keyword arguments as attributes
        self.__dict__.update(kwargs)


if __name__ == "__main__":
    args = Namespace(
        **{
            "max_door_frequency": 5,
            "radius": 15,
            "seed": 2,
            "maze": None,
            "scale": 9,
            "no_gui": True,
            "log_path": "log",
            "disable_logging": False,
            "disable_timeout": True,
            "player": "d",
        }
    )

    root = tk.Tk()
    app = TimingMazeGame(args, root)
