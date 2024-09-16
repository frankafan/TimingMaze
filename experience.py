import constants


class Experience:
    def __init__(self, L, r):
        self.L = L
        self.r = r
        self.cur_pos = (
            0,
            0,
        )  # (x, y) coordinates relative to the original start position
        self.seen_cells = (
            set()
        )  # set of tuples (x, y) storing coordinates of cells relative to the original start position
        self.walls = (
            float("inf"),
            float("inf"),
            float("-inf"),
            float("-inf"),
        )  # (right, top, left, bottom) coordinates relative to the original start position

    def move(self, current_percept):
        """Update experience with new cell seen in this move

        Args:
            current_percept(TimingMazeState): contains current state information
        """

        self.cur_pos = (-current_percept.start_x, -current_percept.start_y)

        # initialize coordinates for the maximum field of view relative to current position
        right, top, left, bottom = 0, 0, 0, 0

        for cell in current_percept.maze_state:

            # update field of view coordinates relative to current position
            right, top, left, bottom = (
                max(right, cell[0]),
                max(top, cell[1]),
                min(left, cell[0]),
                min(bottom, cell[1]),
            )

            cell = (
                cell[0] - current_percept.start_x,
                cell[1] - current_percept.start_y,
            )
            if (cell[0], cell[1]) not in self.seen_cells:
                self.seen_cells.add((cell[0], cell[1]))

        # update walls coordinates relative to the original start position
        if right < self.r:
            self.walls = (
                right + self.cur_pos[0],
                self.walls[1],
                self.walls[2],
                self.walls[3],
            )
        if top < self.r:
            self.walls = (
                self.walls[0],
                top + self.cur_pos[1],
                self.walls[2],
                self.walls[3],
            )
        if left > -self.r:
            self.walls = (
                self.walls[0],
                self.walls[1],
                left + self.cur_pos[0],
                self.walls[3],
            )
        if bottom > -self.r:
            self.walls = (
                self.walls[0],
                self.walls[1],
                self.walls[2],
                bottom + self.cur_pos[1],
            )

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
