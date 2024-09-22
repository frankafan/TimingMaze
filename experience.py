import constants
import random
import numpy as np


class Experience:
    def __init__(self, L, r):
        self.L = L
        self.r = r
        self.num_turns = 0
        self.cur_pos = (
            0,
            0,
        )  # (x, y) coordinates relative to the original start position
        self.maze_dimension = 100  # size of the maze
        self.seen_cells = (
            set()
        )  # set of tuples (x, y) storing coordinates of cells relative to the original start position
        self.walls = (
            float("inf"),
            float("inf"),
            float("-inf"),
            float("-inf"),
        )  # (right, top, left, bottom) coordinates relative to the original start position
        self.stays = {}  # key: (x, y), value: number of stays at the position

        # Hyper-parameters
        self.wait_penalty = 0.2  # penalty for waiting
        self.direction_vector_max_weight = 2  # maximum weight of the direction vector
        self.direction_vector_multiplier = 0.01  # multiplier for the direction vector
        self.direction_vector_weight = min(
            self.direction_vector_max_weight,
            self.direction_vector_multiplier * self.num_turns,
        )  # weight of the direction vector

    def move(self, current_percept):
        """Update experience with new cell seen in this move

        Args:
            current_percept(TimingMazeState): contains current state information
        """

        self.cur_pos = (-current_percept.start_x, -current_percept.start_y)
        self.stays[self.cur_pos] = self.stays.get(self.cur_pos, 0) + 1
        self.num_turns += 1
        self.direction_vector_weight = min(
            self.direction_vector_max_weight,
            self.direction_vector_multiplier * self.num_turns,
        )  # update direction vector weight

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
                self.cur_pos[0] + cell[0],
                self.cur_pos[1] + cell[1],
            )
            if cell not in self.seen_cells:
                self.seen_cells.add(cell)

        # update walls coordinates relative to the original start position
        # TODO: infer left wall from right wall, and bottom wall from top wall
        if right < self.r:
            self.walls = (
                right + self.cur_pos[0],
                self.walls[1],
                right + self.cur_pos[0] - self.maze_dimension,
                self.walls[3],
            )
        if top < self.r:
            self.walls = (
                self.walls[0],
                top + self.cur_pos[1],
                self.walls[2],
                top + self.cur_pos[1] - self.maze_dimension,
            )
        if left > -self.r:
            self.walls = (
                left + self.cur_pos[0] + self.maze_dimension,
                self.walls[1],
                left + self.cur_pos[0],
                self.walls[3],
            )
        if bottom > -self.r:
            self.walls = (
                self.walls[0],
                bottom + self.cur_pos[1] + self.maze_dimension,
                self.walls[2],
                bottom + self.cur_pos[1],
            )

        move = self.get_best_move(current_percept)

        # print(f"Current position: {self.cur_pos}")
        # print(
        #     f"Best move: {'WAIT' if move == constants.WAIT else 'LEFT' if move == constants.LEFT else 'UP' if move == constants.UP else 'RIGHT' if move == constants.RIGHT else 'DOWN'}"
        # )
        # print(f"Walls: {self.walls}")
        # print(f"Number of seen cells: {len(self.seen_cells)}")
        print("\n")

        if self.is_valid_move(current_percept, move):
            return move
        else:
            self.wait()
            return constants.WAIT

    def wait(self):
        """Increment the number of times the player has waited"""
        self.stays[self.cur_pos] = self.stays.get(self.cur_pos, 0) + 1

    def get_direction_vector(self):
        direction_vector = [0, 0]  # [x, y]

        if self.walls[0] > self.maze_dimension or self.walls[1] > self.maze_dimension or self.walls[2] < 0 or self.walls[3] < 0:
            return direction_vector

        for x in range(self.walls[2], self.walls[0]):
            for y in range(self.walls[3], self.walls[1]):
                if (x, y) not in self.seen_cells:
                    direction = (x - self.cur_pos[0], y - self.cur_pos[1])
                    if direction[0] != 0:
                        direction_vector[0] += 1 / direction[0]
                    if direction[1] != 0:
                        direction_vector[1] += 1 / direction[1]

        # Normalize and add weight to direction vector
        direction_vector = (
            np.array(direction_vector)
            / np.linalg.norm(direction_vector)
            * self.direction_vector_weight
        )

        return direction_vector

    def get_best_move(self, current_percept):
        """Evaluate best move

        Returns:
            int:
                WAIT = -1
                LEFT = 0
                UP = 1
                RIGHT = 2
                DOWN = 3
        """
        move_scores = self.get_move_scores()

        # Normalize move scores
        for i in range(4):
            move_scores[i] = move_scores[i] / max([1, max(move_scores)])

        direction_vector = self.get_direction_vector()

        for i in range(4):
            # Give penalty for waiting
            if not self.is_valid_move(current_percept, i):
                move_scores[i] = move_scores[i] - self.wait_penalty * self.stays.get(
                    self.cur_pos, 0
                )

            # Add direction vector to move scores
            if i == constants.LEFT:
                move_scores[i] -= direction_vector[0]
                move_scores[i] -= (
                    self.stays.get((self.cur_pos[0] - 1, self.cur_pos[1]), 0)
                    * self.wait_penalty
                )
            elif i == constants.UP:
                move_scores[i] -= direction_vector[1]
                move_scores[i] -= (
                    self.stays.get((self.cur_pos[0], self.cur_pos[1] - 1), 0)
                    * self.wait_penalty
                )
            elif i == constants.RIGHT:
                move_scores[i] += direction_vector[0]
                move_scores[i] -= (
                    self.stays.get((self.cur_pos[0] + 1, self.cur_pos[1]), 0)
                    * self.wait_penalty
                )
            elif i == constants.DOWN:
                move_scores[i] += direction_vector[1]
                move_scores[i] -= (
                    self.stays.get((self.cur_pos[0], self.cur_pos[1] + 1), 0)
                    * self.wait_penalty
                )

        max_score = max(move_scores)
        max_indices = [i for i, score in enumerate(move_scores) if score == max_score]
        move = random.choice(max_indices)

        print(f"Direction vector: {direction_vector}")
        print(f"Direction vector weight: {self.direction_vector_weight}")
        print(f"Move scores: {move_scores}")
        return move

    def get_move_scores(self):
        """Score each move based on the number of new cells seen

        Returns:
            list: list of scores for each move (LEFT, UP, RIGHT, DOWN)
        """
        move_scores = [0, 0, 0, 0]

        for dx, dy in [
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1),
        ]:  # LEFT, UP, RIGHT, DOWN
            num_new_cells = self.get_num_new_cells(
                self.cur_pos[0] + dx, self.cur_pos[1] + dy
            )
            if dx == -1 and dy == 0:
                move_scores[constants.LEFT] = num_new_cells
            elif dx == 0 and dy == -1:
                move_scores[constants.UP] = num_new_cells
            elif dx == 1 and dy == 0:
                move_scores[constants.RIGHT] = num_new_cells
            elif dx == 0 and dy == 1:
                move_scores[constants.DOWN] = num_new_cells
        return move_scores

    def get_num_new_cells(self, x, y):
        """Get the number of new cells seen at a new position

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

    # TODO: This function can be sped up by decreasing the number iterations
    def is_valid_move(self, current_percept, move):
        direction = [0, 0, 0, 0]
        for maze_state in current_percept.maze_state:
            if maze_state[0] == 0 and maze_state[1] == 0:
                direction[maze_state[2]] = maze_state[3]

        if direction[move] != constants.OPEN:
            return False

        if move == constants.LEFT:
            for maze_state in current_percept.maze_state:
                if (
                    maze_state[0] == -1
                    and maze_state[1] == 0
                    and maze_state[2] == constants.RIGHT
                    and maze_state[3] == constants.OPEN
                ):
                    return True
        elif move == constants.UP:
            for maze_state in current_percept.maze_state:
                if (
                    maze_state[0] == 0
                    and maze_state[1] == -1
                    and maze_state[2] == constants.DOWN
                    and maze_state[3] == constants.OPEN
                ):
                    return True
        elif move == constants.RIGHT:
            for maze_state in current_percept.maze_state:
                if (
                    maze_state[0] == 1
                    and maze_state[1] == 0
                    and maze_state[2] == constants.LEFT
                    and maze_state[3] == constants.OPEN
                ):
                    return True
        elif move == constants.DOWN:
            for maze_state in current_percept.maze_state:
                if (
                    maze_state[0] == 0
                    and maze_state[1] == 1
                    and maze_state[2] == constants.UP
                    and maze_state[3] == constants.OPEN
                ):
                    return True

        return False
