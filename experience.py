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

        best_move = self.get_best_move()
        return best_move

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
        max_new_cells = 0
        best_move = constants.WAIT

        for dx, dy in [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
        ]:  # UP, RIGHT, DOWN, LEFT
            num_new_cells = self.get_num_new_cells(
                self.cur_pos[0] + dx, self.cur_pos[1] + dy
            )
            if num_new_cells > max_new_cells:
                max_new_cells = num_new_cells
                if dx == 0 and dy == 1:
                    best_move = constants.UP
                elif dx == 1 and dy == 0:
                    best_move = constants.RIGHT
                elif dx == 0 and dy == -1:
                    best_move = constants.DOWN
                elif dx == -1 and dy == 0:
                    best_move = constants.LEFT

        return best_move

    def get_num_new_cells(self, x, y):
        """Get the number of new cells at a new position

        Args:
            x (int): x-coordinate of the new position
            y (int): y-coordinate of the new position

        Returns:
            int: number of new cells seen at the new position
        """

        num_new_cells = 0
        for dx in range(-self.r, self.r + 1):
            for dy in range(-self.r, self.r + 1):
                if dx**2 + dy**2 <= self.r**2:
                    if (x + dx, y + dy) not in self.seen_cells and (
                        self.walls[2] <= x + dx <= self.walls[0]
                        and self.walls[3] <= y + dy <= self.walls[1]
                    ):
                        num_new_cells += 1
        return num_new_cells
