import pygame as pg
from pygame.sprite import Sprite
from pygame import gfxdraw


class SolveButton(Sprite):
    def __init__(self, pos, size, text, callback):
        super().__init__()
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.text = text
        self.callback = callback
        self._render()

    def _render(self):
        W, H = self.rect.size
        self.image.fill((50, 20, 200))
        font = pg.font.SysFont(None, 24)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(W // 2, H // 2))
        self.image.blit(text_surf, text_rect)

    def on_click(self):
        print("Solve button clicked")
        self.callback()