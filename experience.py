import constants


class Experience:
    def __init__(self, L, r):
        self.L = L
        self.r = r
        self.cur_pos = (0, 0)
        self.seen_cells = (
            set()
        )  # set of tuples (x, y) storing coordinates of cells relative to the original start position

    def move(self, current_percept):
        """Update experience with new cell seen in this move

        Args:
            current_percept(TimingMazeState): contains current state information
        """

        self.cur_pos = (-current_percept.start_x, -current_percept.start_y)
        for cell in current_percept.maze_state:
            cell = (
                cell[0] - current_percept.start_x,
                cell[1] - current_percept.start_y,
            )
            if (cell[0], cell[1]) not in self.seen_cells:
                self.seen_cells.add((cell[0], cell[1]))

    def get_best_move(self):
        """Get the move that maximizes the number of new cells seen

        Returns:
            int:
                WAIT = -1
                LEFT = 0
                UP = 1
                RIGHT = 2
                DOWN = 3
        """
