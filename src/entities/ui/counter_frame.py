import pygame as pg
from pygame.sprite import Sprite
from pygame import gfxdraw


class CounterFrame(Sprite):
    def __init__(self, size, top_left_pos, screen):
        super().__init__()
        self.screen = screen
        self.size = size
        self._counter = 0
        self.image = self._create_image()
        self.rect = self.image.get_rect(topleft=top_left_pos)

    @property
    def counter(self):
        return self._counter

    def set_counter(self, new_val: int):
        """
        Set the counter to a specific value.
        """
        self._counter = new_val
        self._update_image()

    def increase(self):
        """
        Increment the counter by 1.
        """
        self._counter += 1
        self._update_image()

    def decrease(self):
        self._counter -= 1
        self._update_image()

    def reset(self):
        """
        Reset the counter to 0.
        """
        self._counter = 0
        self._update_image()

    def _create_image(self):
        """
        Create an image with a counter frame.
        """
        W, H = self.size
        surf = pg.Surface((W, H), pg.SRCALPHA)
        # Draw the frame
        gfxdraw.filled_polygon(surf, [
            (0, 0), (W, 0), (W, H), (0, H)
        ], (255, 255, 255, 200))
        # Draw the counter text
        font = pg.font.SysFont(None, 36)
        text_surf = font.render(str(self._counter) + " mov", True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(W // 2, H // 2))
        surf.blit(text_surf, text_rect)

        return surf

    def _update_image(self):
        """
        Update the image to reflect the current counter value.
        """
        self.image = self._create_image()
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.screen.blit(self.image, self.rect)


