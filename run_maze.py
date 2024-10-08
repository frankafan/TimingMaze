from timing_maze_game import TimingMazeGame
import tkinter as tk
import sys

sys.setrecursionlimit(10000)

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


if __name__ == "__main__":
    args = Namespace(
        **{
            "max_door_frequency": 3,
            "radius": 30,
            "seed": 3,
            "maze": None,
            "scale": 9,
            "no_gui": True,
            "log_path": "",
            "disable_logging": True,
            "disable_timeout": True,
            "player": "1",
        }
    )

    root = tk.Tk()
    app = TimingMazeGame(args, root)
