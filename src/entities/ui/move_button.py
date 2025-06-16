import pygame as pg


class MoveButton(pg.sprite.Sprite):
    def __init__(self, pos, size, text, callback):
        super().__init__()
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.text = text
        self.callback = callback

        self._render()

    def _render(self):
        self.image.fill((50, 200, 50))
        font = pg.font.SysFont(None, 28)
        text_surf = font.render(self.text, True, (255, 255, 255))
        self.image.blit(text_surf, text_surf.get_rect(center=(self.rect.width//2, self.rect.height//2)))

    def on_click(self):
        self.callback()
