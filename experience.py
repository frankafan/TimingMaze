class Experience:
    def __init__(self, L, r):
        self.L = L
        self.r = r
        self.seen_cells = (
            set()
        )  # set of tuples (x, y) storing coordinates of cells relative to the original start position

    def move(self, current_percept):
        """Update experience with new cell seen in this move

        Args:
            current_percept(TimingMazeState): contains current state information
        """

        for cell in current_percept.maze_state:
            if (cell[0], cell[1]) not in self.seen_cells:
                self.seen_cells.add((cell[0], cell[1]))
