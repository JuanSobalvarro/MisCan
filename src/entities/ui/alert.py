import pygame as pg
from pygame.sprite import Sprite
from pygame import gfxdraw

class Alert(Sprite):
    def __init__(self, pos, size, color, text, callback=None, text_size=28, radius=12):
        super().__init__()
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.callback = callback            # Callback when alert is shown
        self.text_size = text_size
        self.radius = radius

        self.image = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self._render()

        self.visible = False
        self.hide_time = None
        self.show_callback = None          # Callback to run when alert hides

    def set_text(self, new_text):
        """
        Update the alert text and re-render the surface.
        """
        self.text = new_text
        self._render()


    def show(self, timeout_ms=None, on_hide_callback=None):
        """
        Show the alert, optionally auto-hide after timeout_ms milliseconds,
        and optionally execute on_hide_callback when it hides.
        """
        self.visible = True
        if self.callback:
            self.callback()
        self.show_callback = on_hide_callback
        if timeout_ms:
            self.hide_time = pg.time.get_ticks() + timeout_ms
        else:
            self.hide_time = None

    def hide(self):
        """
        Hide the alert immediately and run the show_callback if set.
        """
        if self.visible and self.show_callback:
            self.show_callback()
            self.show_callback = None  # Ensure callback runs only once
        self.visible = False
        self.hide_time = None

    def update(self, *args):
        """
        Call this in your main loop to auto-hide when timeout is reached.
        """
        if self.visible and self.hide_time and pg.time.get_ticks() >= self.hide_time:
            self.hide()

    def draw(self, surface):
        """
        Draw the alert on the given surface if visible.
        """
        if self.visible:
            surface.blit(self.image, self.rect)

    def on_click(self, event):
        """
        Hide the alert if clicked.
        """
        if self.visible and self.rect.collidepoint(event.pos):
            self.hide()

    def _render(self):
        """
        Pre-render the alert surface with text and rounded corners.
        """
        self.image.fill((0, 0, 0, 0))  # Clear previous content
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
