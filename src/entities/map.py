from typing import Tuple
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame import gfxdraw
import math
import random

class Map(Sprite):
    def __init__(self, size: Tuple[int, int], land_color, water_color, shore_color,
                 river_width=80, shore_width=20, wavy_frequency=1, wavy_amplitude=100):
        super().__init__()
        self.counter = 0

        # Parameters for river
        self.river_width = river_width
        self.shore_width = shore_width
        self.wavy_amplitude = wavy_amplitude
        self.wavy_frequency = wavy_frequency

        # Parameters for shore independent movement
        self.shore_amplitude = wavy_amplitude * 0.5
        self.shore_frequency = wavy_frequency * 0.8
        self.shore_phase_offset_left = random.uniform(0, 1000)
        self.shore_phase_offset_right = random.uniform(0, 1000)

        self.size = size
        self.land_color = land_color
        self.water_color = water_color
        self.shore_color = shore_color

        self.image = self._generate_landscape()
        self.rect = self.image.get_rect()

    def _generate_landscape(self) -> Surface:
        surface = Surface(self.size)
        surface.fill(self.land_color)
        self._generate_river(surface)
        return surface

    def _generate_river(self, surface):
        left_edge = self._wavy_line_left()
        right_edge = self._wavy_line_right()

        river_polygon = left_edge + right_edge[::-1]

        # === Draw filled river polygon ===
        gfxdraw.filled_polygon(surface, river_polygon, self.water_color)
        gfxdraw.aapolygon(surface, river_polygon, self.water_color)

        # === Draw shores along left and right edges ===
        shore_left = self._generate_independent_shore(left_edge, self.shore_phase_offset_left)
        shore_right = self._generate_independent_shore(right_edge, self.shore_phase_offset_right)

        left_shore_polygon = left_edge + shore_left[::-1]
        gfxdraw.aapolygon(surface, left_shore_polygon, self.shore_color)
        gfxdraw.filled_polygon(surface, left_shore_polygon, self.shore_color)

        right_shore_polygon = right_edge + shore_right[::-1]
        gfxdraw.aapolygon(surface, right_shore_polygon, self.shore_color)
        gfxdraw.filled_polygon(surface, right_shore_polygon, self.shore_color)

    def _generate_independent_shore(self, edge_points, phase_offset):
        """
        Generate shore edge with its own wavy movement, independent from the river.
        """
        new_edge = []
        for (x, y) in edge_points:
            wave = math.sin((y + self.counter + phase_offset) / self.shore_frequency) * self.shore_amplitude
            # Move outward from the river edge depending on the sign of x (left or right)
            direction = -1 if x < self.size[0] // 2 else 1
            new_edge.append((x + direction * (self.shore_width + wave), y))
        return new_edge

    def _wavy_line_left(self):
        return self._generate_wavy_line(-self.river_width // 2)

    def _wavy_line_right(self):
        return self._generate_wavy_line(self.river_width // 2)

    def _generate_wavy_line(self, horizontal_offset=0):
        points = []
        for y in range(0, self.size[1], 5):
            wavywavy = math.sin((y + self.counter) / self.wavy_frequency) + math.sin((2 * y + self.counter) / self.wavy_frequency ) / 5
            x = int(wavywavy * self.wavy_amplitude + self.size[0] // 2)
            points.append((x + horizontal_offset, y))
        return points

    def update(self, *args, **kwargs):
        self.counter = (self.counter + 2) % 10000
        self.image = self._generate_landscape()
