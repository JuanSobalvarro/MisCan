import pygame as pg
from pygame import gfxdraw

class ObjectiveSprite(pg.sprite.Sprite):
    def __init__(self, pos, size, callback, parent):
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
        self._draw_objective()

    def is_expanded(self):
        """Returns whether the sprite is expanded to match the parent's size."""
        return self._expanded

    def on_click(self):
        """Handles click events on the sprite."""
        if self.callback:
            self.callback(self)

    def expand_on_parent(self):
        """Expands the sprite to match the parent's size."""
        parent = self.parent
        if parent:
            self.rect.size = (parent.rect.size[0] - 2 * self.margins[0], parent.rect.size[1] - 2 * self.margins[1])
            self.image = pg.Surface(self.rect.size, pg.SRCALPHA)
            self.rect.topleft = (self.parent.rect.left + self.margins[0], self.parent.rect.top + self.margins[1]) if self.parent else (0, 0)
            self._expanded = True
            self._draw_objective()

    def unexpand_on_parent(self):
        """Unexpands the sprite to its original size."""
        self.rect.size = self.original_size
        self.image = pg.Surface(self.original_size, pg.SRCALPHA)
        self.rect.topleft = self.original_pos
        self._expanded = False
        self._draw_objective()

    def _draw_objective(self):
        W, H = self.rect.size
        circle_radius = min(W, H) // 10
        triangle_offset = min(W, H) // 10

        # Clear the main image with a semi-transparent background
        self.image.fill((240, 240, 240, self.transparency))

        # Draw river (blue rectangle)
        river_rect = pg.Rect(W // 3, 0, W // 3, H)
        pg.draw.rect(self.image, (0, 0, 255, self.transparency), river_rect)

        # Create transparent temporary surface for antialiased shapes
        shape_surface = pg.Surface((W, H), pg.SRCALPHA)

        # Cannibals: red circles drawn on temp surface
        for i in range(3):
            cx = W // 6
            cy = H // 6 + i * H // 3
            gfxdraw.aacircle(shape_surface, cx, cy, circle_radius, (200, 0, 0, self.transparency))
            gfxdraw.filled_circle(shape_surface, cx, cy, circle_radius, (200, 0, 0, self.transparency))

        # Missionaries: black triangles drawn on temp surface
        for i in range(3):
            cy = H // 6 + i * H // 3
            points = [(W - W // 6, cy - triangle_offset), (W - W // 6 - triangle_offset, cy + triangle_offset), (W - W // 6 + triangle_offset, cy + triangle_offset)]
            gfxdraw.aapolygon(shape_surface, points, (0, 0, 0, self.transparency))
            gfxdraw.filled_polygon(shape_surface, points, (0, 0, 0, self.transparency))

        # Blit the transparent shape_surface on top of the main image
        self.image.blit(shape_surface, (0, 0))

