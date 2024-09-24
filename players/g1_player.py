import os
import pickle
import numpy as np
import logging

import constants
from timing_maze_state import TimingMazeState
from experience import Experience


class Player:
    def __init__(
        self,
        rng: np.random.Generator,
        logger: logging.Logger,
        precomp_dir: str,
        maximum_door_frequency: int,
        radius: int,
        wait_penalty: int,
        revisit_penalty: int,
        revisit_max_penalty: int,
        direction_vector_max_weight: int,
        direction_vector_multiplier: int,
        direction_vector_pov_radius: int,
    ) -> None:
        """Initialise the player with the basic amoeba information

        Args:
            rng (np.random.Generator): numpy random number generator, use this for same player behavior across run
            logger (logging.Logger): logger use this like logger.info("message")
            maximum_door_frequency (int): the maximum frequency of doors
            radius (int): the radius of the drone
            precomp_dir (str): Directory path to store/load pre-computation
        """

        self.rng = rng
        self.logger = logger
        self.maximum_door_frequency = maximum_door_frequency
        self.radius = radius
        self.experience = Experience(
            self.maximum_door_frequency,
            self.radius,
            wait_penalty=wait_penalty,
            revisit_penalty=revisit_penalty,
            revisit_max_penalty=revisit_max_penalty,
            direction_vector_max_weight=direction_vector_max_weight,
            direction_vector_multiplier=direction_vector_multiplier,
            direction_vector_pov_radius=direction_vector_pov_radius,
        )

    def move(self, current_percept) -> int:
        """Function which retrieves the current state of the amoeba map and returns an amoeba movement

        Args:
            current_percept(TimingMazeState): contains current state information
        Returns:
            int: This function returns the next move of the user:
                WAIT = -1
                LEFT = 0
                UP = 1
                RIGHT = 2
                DOWN = 3
        """
        return self.experience.move(current_percept)
