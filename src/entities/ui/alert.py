import pygame as pg
from pygame.sprite import Sprite
from pygame import gfxdraw


class Alert(Sprite):
    def __init__(self, pos, size, color, text, callback=None, text_size=28, radius=12):
        super().__init__()
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.text = text
        self.color = color
        self.callback = callback
        self.text_size = text_size
        self.radius = radius
        self.visible = False
        self._render()

    def show_alert_ms(self, surface, time_ms: int):
        """
        Display the alert for a specified duration in milliseconds.
        """
        self.visible = True
        if self.callback:
            # Call the callback function if provided
            self.callback()
        self._render()
        surface.blit(self.image, self.rect)
        pg.display.update(self.rect)
        pg.time.delay(time_ms)
        self.hide_alert(surface)

    def hide_alert(self, surface):
        """
        Hide the alert by filling the area with a transparent color.
        """
        self.visible = False
        surface.fill((0, 0, 0, 0), self.rect)  # Fill with transparent in case you have alpha surface
        pg.display.update(self.rect)

    def on_click(self, event):
        """
        Call the callback if the alert was clicked.
        """
        if self.visible and self.rect.collidepoint(event.pos):
            if self.callback:
                self.callback()
            self.hide_alert()

    def _render(self):
        """
        Render the alert surface with text and rounded corners.
        """
        self.image.fill((0, 0, 0, 0))  # Clear previous content

        # Draw rounded rectangle background
        self._draw_rounded_rect(self.image, self.color, self.image.get_rect(), self.radius)

        # Render text
        font = pg.font.SysFont(None, self.text_size)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(text_surf, text_rect)

    def _draw_rounded_rect(self, surface, color, rect, radius):
        """
        Draw a rounded rectangle using gfxdraw for smoothness.
        """
        x, y, w, h = rect
        gfxdraw.aacircle(surface, x + radius, y + radius, radius, color)
        gfxdraw.filled_circle(surface, x + radius, y + radius, radius, color)

        gfxdraw.aacircle(surface, x + w - radius - 1, y + radius, radius, color)
        gfxdraw.filled_circle(surface, x + w - radius - 1, y + radius, radius, color)

        gfxdraw.aacircle(surface, x + radius, y + h - radius - 1, radius, color)
        gfxdraw.filled_circle(surface, x + radius, y + h - radius - 1, radius, color)

        gfxdraw.aacircle(surface, x + w - radius - 1, y + h - radius - 1, radius, color)
        gfxdraw.filled_circle(surface, x + w - radius - 1, y + h - radius - 1, radius, color)

        pg.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
        pg.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
