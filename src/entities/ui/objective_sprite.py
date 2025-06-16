import pygame as pg
from pygame import gfxdraw
from src.entities.state import State
from src.enums import Shores

class ObjectiveSprite(pg.sprite.Sprite):
    def __init__(self, objective_state: State, pos, size, callback, parent):
        super().__init__()
        self.parent = parent
        self.margins = (self.parent.rect.width // 40, self.parent.rect.height // 40) if parent else (0, 0)
        self.original_size = size
        self.original_pos = pos
        self.transparency = 220
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.callback = callback
        self._expanded = False
        self.objective_state = objective_state
        self._draw_objective()

    def is_expanded(self):
        return self._expanded

    def on_click(self):
        if self.callback:
            self.callback(self)

    def expand_on_parent(self):
        if self.parent:
            self.rect.size = (
                self.parent.rect.width - 2 * self.margins[0],
                self.parent.rect.height - 2 * self.margins[1]
            )
            self.image = pg.Surface(self.rect.size, pg.SRCALPHA)
            self.rect.topleft = (
                self.parent.rect.left + self.margins[0],
                self.parent.rect.top + self.margins[1]
            )
            self._expanded = True
            self._draw_objective()

    def unexpand_on_parent(self):
        self.rect.size = self.original_size
        self.image = pg.Surface(self.original_size, pg.SRCALPHA)
        self.rect.topleft = self.original_pos
        self._expanded = False
        self._draw_objective()

    def _draw_objective(self):
        W, H = self.rect.size
        circle_radius = min(W, H) // 12
        triangle_offset = min(W, H) // 12

        # Clear background
        self.image.fill((240, 240, 240, self.transparency))

        # Draw river
        river_rect = pg.Rect(W // 3, 0, W // 3, H)
        pg.draw.rect(self.image, (0, 0, 255, self.transparency), river_rect)

        # Transparent surface for antialiased shapes
        shape_surface = pg.Surface((W, H), pg.SRCALPHA)

        # Unpack objective counts
        (left_m, left_c), (right_m, right_c) = self.objective_state.objective_state

        # Positions for drawing entities
        side_x_positions = {
            Shores.LEFT: W // 6,
            Shores.RIGHT: W - W // 6
        }

        def draw_cannibals(side, count):
            cx = side_x_positions[side]
            for i in range(count):
                cy = H // 6 + i * H // 5
                gfxdraw.aacircle(shape_surface, cx, cy, circle_radius, (200, 0, 0, self.transparency))
                gfxdraw.filled_circle(shape_surface, cx, cy, circle_radius, (200, 0, 0, self.transparency))

        def draw_missionaries(side, count):
            cx = side_x_positions[side]
            for i in range(count):
                cy = H // 6 + i * H // 5
                points = [
                    (cx, cy - triangle_offset),
                    (cx - triangle_offset, cy + triangle_offset),
                    (cx + triangle_offset, cy + triangle_offset)
                ]
                gfxdraw.aapolygon(shape_surface, points, (0, 0, 0, self.transparency))
                gfxdraw.filled_polygon(shape_surface, points, (0, 0, 0, self.transparency))

        # Draw left side
        draw_cannibals(Shores.LEFT, left_c)
        draw_missionaries(Shores.LEFT, left_m)

        # Draw right side
        draw_cannibals(Shores.RIGHT, right_c)
        draw_missionaries(Shores.RIGHT, right_m)

        # Blit to final surface
        self.image.blit(shape_surface, (0, 0))
