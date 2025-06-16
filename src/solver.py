"""
This module provides a solver for the missionaries and cannibals problem.
"""
from typing import List, Tuple
from collections import deque

from src.entities.state import State
from src.enums import Shores


class Solver:

    @staticmethod
    def solve_from_state(initial_state: State) -> List[State]:
        """
        Solve the missionaries and cannibals problem from the given initial state.
        Returns the sequence of states leading to the solution.
        """
        visited = set()
        queue = deque()
        queue.append((initial_state, []))

        while queue:
            current_state, path = queue.popleft()

            state_id = (current_state.missionaries_left, current_state.cannibals_left, current_state.boat_position)
            if state_id in visited:
                continue
            visited.add(state_id)

            if current_state.is_objective():
                # Rebuild the path to include counters for animation
                return Solver.rebuild_path(path + [current_state])

            for next_state in Solver.get_next_states(current_state):
                queue.append((next_state, path + [current_state]))

        return []

    @staticmethod
    def rebuild_path(path: List[State]) -> List[State]:
        """
        Sets the counter properly in the solution path.
        """
        new_path = []
        for i, state in enumerate(path):
            state.counter = i
            new_path.append(state)
        return new_path

    @staticmethod
    def get_next_states(current_state: State) -> List[State]:
        """
        Generate all possible next valid states from the current state.
        """
        next_states = []
        for m in range(3):
            for c in range(3):
                if m + c == 0 or m + c > 2:
                    continue

                if current_state.boat_position == Shores.LEFT:
                    new_m_left = current_state.missionaries_left - m
                    new_c_left = current_state.cannibals_left - c
                    new_boat_position = Shores.RIGHT
                else:
                    new_m_left = current_state.missionaries_left + m
                    new_c_left = current_state.cannibals_left + c
                    new_boat_position = Shores.LEFT

                new_state = State(
                    missionaries_left=new_m_left,
                    cannibals_left=new_c_left,
                    objective_state=current_state.objective_state,
                    boat_position=new_boat_position,
                    counter=0  # Will be set in rebuild_path()
                )

                if new_state.is_valid() and Solver.is_within_bounds(new_m_left, new_c_left):
                    next_states.append(new_state)

        return next_states

    @staticmethod
    def is_within_bounds(m_left, c_left) -> bool:
        return 0 <= m_left <= 3 and 0 <= c_left <= 3
