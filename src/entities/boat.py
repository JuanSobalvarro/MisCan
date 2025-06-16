import pygame
from pygame import Surface, gfxdraw
from typing import Tuple
from src.enums import Shores
from src.entities.npc import NPC


class Boat(pygame.sprite.Sprite):
    def __init__(self, left_pos: Tuple[int, int], right_pos: Tuple[int, int], start_pos: int,
                 dimensions: Tuple[int, int], start_shore: Shores = Shores.LEFT):
        super().__init__()
        self.start_pos = start_pos
        self.left_pos = left_pos
        self.right_pos = right_pos
        self.dimensions = dimensions
        self.start_shore = start_shore
        self.current_shore = start_shore

        self.image = self._create_image(dimensions)
        self.rect = self.image.get_rect()

        self.passengers: list[NPC, NPC] = []

        # Set start position
        self.set_position(start_pos)

    def reset_boat(self):
        self.passengers.clear()
        self.set_position(self.start_pos)
        self.current_shore = self.start_shore

    def _rearrange_passengers(self):
        """
        Rearranges passengers in the boat to maintain order.
        This is a placeholder for future logic if needed.
        """
        boat_size = len(self.passengers)
        if boat_size > 0:
            self.passengers = sorted(self.passengers)

            for i, passenger in enumerate(self.passengers, 0):
                # Update passenger position based on their index in the boat
                print(f"Moving {passenger} to position {i}")
                passenger.move((self.rect.left + self.rect.width // 2 * i,
                                self.rect.top - passenger.dimensions[1]))


    def add_passenger(self, passenger: NPC):
        """
        Adds a passenger to the boat if there's space.
        """
        if passenger.shore != self.current_shore:
            print(f"Passenger {passenger.shore} is not on the same shore as the boat {self.current_shore}.")
            print(f"Passengers on boat: {self.passengers}")
            return False

        boat_size = len(self.passengers)
        if boat_size < 2:
            self.passengers.append(passenger)

            # Move passenger to the boat's position
            passenger.move((self.rect.left + self.rect.width // 2 * boat_size,
                            self.rect.top - passenger.dimensions[1]))

            return True

        return False

    def remove_passenger(self, passenger: NPC):
        """
        Removes a passenger from the boat.
        """
        if passenger in self.passengers:
            passenger.get_down(self.current_shore)

            self.passengers.remove(passenger)

            self._rearrange_passengers()
            return True

        return False

    def _create_image(self, dimensions: Tuple[int, int]) -> Surface:
        """
        Creates the boat surface with a simple rectangle and wooden texture.
        """
        width, height = dimensions
        surface = Surface((width, height), pygame.SRCALPHA)
        boat_color = (111, 66, 36)  # "#6f4224"
        line_color = (78, 50, 32)   # "#4e3220"
        bow_color = (139, 69, 19)   # "#8b4513"

        surface.fill(boat_color)

        # Add lines to simulate wood texture
        for i in range(0, width, 10):
            gfxdraw.line(surface, i, 0, i, height, line_color)
        for j in range(0, height, 10):
            gfxdraw.line(surface, 0, j, width, j, line_color)

        # Draw bow (triangle at the front)
        bow_points = [(width // 2, 0), (0, height), (width, height)]
        gfxdraw.filled_polygon(surface, bow_points, bow_color)
        gfxdraw.aapolygon(surface, bow_points, bow_color)

        return surface

    def set_position(self, position: int):
        """
        Sets the boat position to LEFT, MIDDLE, or RIGHT.
        """
        if position == Shores.LEFT:
            self.rect.topleft = self.left_pos
        elif position == Shores.RIGHT:
            self.rect.topleft = self.right_pos

    def move(self):
        """
        Public method to move the boat.
        """
        boat_occupants = len(self.passengers)
        if boat_occupants == 0:
            print(f"Boat cannot move without passengers.")
            return False

        self.current_shore = Shores.RIGHT if self.current_shore == Shores.LEFT else Shores.LEFT

        self.set_position(self.current_shore)

        # Move passengers to the new shore
        for passenger in self.passengers:
            passenger.get_down(self.current_shore)

        self.passengers.clear()

        print(f"Boat moved to {self.current_shore} shore with {boat_occupants} passengers.")
        return True

