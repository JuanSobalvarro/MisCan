from typing import Tuple
from src.enums import Shores, NPCType


class State:
    def __init__(self, missionaries_left, cannibals_left, objective_state: Tuple[Tuple[int, int], Tuple[int, int]], boat_position: Shores, counter):
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.boat_position = boat_position  # "left" or "right"
        self.objective_state = objective_state
        self.counter = counter

    @property
    def missionaries_right(self) -> int:
        return 3 - self.missionaries_left

    @property
    def cannibals_right(self) -> int:
        return 3 - self.cannibals_left

    def update_state(self, missionaries_left: int, cannibals_left: int, boat_position: Shores, counter: int):
        """
        Update the state with new values.
        """
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.boat_position = boat_position
        self.counter = counter

    def is_objective(self):
        # Check if all missionaries and cannibals are on the right side
        if self.missionaries_left != self.objective_state[0][0]:
            return False

        if self.cannibals_left != self.objective_state[0][1]:
            return False

        if self.missionaries_right != self.objective_state[1][0]:
            return False

        if self.cannibals_right != self.objective_state[1][1]:
            return False

        return True

    def is_valid(self):
        # Validate the state: no side should have more cannibals than missionaries
        if self.cannibals_left > self.missionaries_left and self.missionaries_left > 0:
            return False
        if self.cannibals_right > self.missionaries_right and self.missionaries_right > 0:
            return False
        return True

    def __repr__(self):
        return f"State({self.missionaries_left}, {self.cannibals_left}, {self.boat_position})"
