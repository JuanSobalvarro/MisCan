from typing import Tuple
from src.enums import Shores
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame import gfxdraw
import pygame as pg
from src.enums import NPCType, MissionaryColors, CannibalColors


class NPC(Sprite):
    def __init__(self, right_shore_pos, left_shore_pos, dimensions: Tuple[float, float],
                 npc_type: NPCType, start_shore: Shores, screen: Surface):
        super().__init__()
        self.dimensions = dimensions
        self.screen = screen
        self.npc_type = npc_type
        self.start_shore = start_shore
        self.current_shore = start_shore
        self.right_shore_pos = right_shore_pos
        self.left_shore_pos = left_shore_pos

        self.image = self._create_image()
        self.rect = self.image.get_rect(topleft=right_shore_pos if start_shore == Shores.RIGHT else left_shore_pos)

    @property
    def start_pos(self) -> Tuple[int, int]:
        """
        Get the starting position of the NPC based on its current shore.
        """
        return self.right_shore_pos if self.start_shore == Shores.RIGHT else self.left_shore_pos

    @property
    def shore(self):
        return self.current_shore

    def _create_image(self) -> Surface:
        """
        Create an image with more detailed shapes and antialiasing.
        """
        W, H = map(int, self.dimensions)
        surf = Surface((W, H), pg.SRCALPHA)

        # draw entity box
        gfxdraw.box(surf, pg.Rect(0, 0, W, H), (255, 0, 0, 100))  # transparent box

        # === Body ===
        self._figure(surf)

        return surf

    def move(self, coords: Tuple[int, int]):
        """
        Move the NPC to the specified coordinates.
        """
        self.rect.topleft = coords

    def reset_position(self):
        """
        Reset the NPC's position to its starting position.
        """
        self.move(self.start_pos)
        self.current_shore = self.start_shore

    def get_down(self, shore: Shores):
        self.current_shore = shore
        pos = self.right_shore_pos if shore == Shores.RIGHT else self.left_shore_pos

        # Move the NPC to the shore position
        self.move(pos)

    def _figure(self, surface):
        """
        Draw the body of the NPC over the surface.
        """
        body_width = self.dimensions[0] // 10
        body_height = self.dimensions[1] // 2
        head_radius = self.dimensions[1] // 7
        head_center = (self.dimensions[0] // 2, head_radius)
        eye_radius = max(1, self.dimensions[0] // 25)
        eye_y = head_center[1] - eye_radius
        eye_offset = self.dimensions[0] // 10
        arm_width = body_height // 2
        arm_height = body_width // 2
        leg_width = body_width // 2
        leg_height = body_height // 2 + body_height // 3
        arm_y = head_center[1] + head_radius + body_height // 4

        if self.npc_type == NPCType.MISSIONARY:

            # Draw head
            self._draw_head(surface, head_center, head_radius, MissionaryColors.SKIN_TONE.value)

            # eyes
            self._draw_eyes(surface, head_center, eye_radius, eye_y, eye_offset, MissionaryColors.EYE_COLOR.value)

            # arms
            self._draw_arms(surface, head_center, body_width, body_height, arm_y, MissionaryColors.SKIN_TONE.value)

            # draw stick figure body
            self._draw_body(surface, head_center, head_radius, body_width, body_height, MissionaryColors.SHIRT_COLOR.value)


            # legs
            self._draw_legs(surface, head_center, head_radius, body_width, body_height, leg_width, leg_height, MissionaryColors.PANTS_COLOR.value)

            # draw bible with crux on left arm
            bible_width = body_width
            bible_height = body_height // 2
            bible_rect = pg.Rect(head_center[0] - arm_width - body_width, arm_y - bible_height // 2,
                                 bible_width, bible_height)
            gfxdraw.box(surface, bible_rect, MissionaryColors.BIBLE_COLOR.value)

        elif self.npc_type == NPCType.CANNIBAL:

            # draw head
            self._draw_head(surface, head_center, head_radius, CannibalColors.SKIN_TONE.value)

            # draw eyes
            self._draw_eyes(surface, head_center, eye_radius, eye_y, eye_offset, CannibalColors.EYE_COLOR.value)

            # draw mouth
            mouth_rect = pg.Rect(head_center[0] - self.dimensions[0] // 8,
                                 head_center[1] + head_radius // 2,
                                 self.dimensions[0] // 4, self.dimensions[1] // 20)
            gfxdraw.box(surface, mouth_rect, CannibalColors.MOUTH_COLOR.value)

            # Draw body
            self._draw_body(surface, head_center, head_radius, body_width, body_height, CannibalColors.SKIN_TONE.value)

            # draw arms
            self._draw_arms(surface, head_center, body_width, body_height, arm_y, CannibalColors.SKIN_TONE.value)

            # draw legs
            self._draw_legs(surface, head_center, head_radius, body_width, body_height, leg_width, leg_height, CannibalColors.PANTS_COLOR.value)

            # Draw bone spear in arm
            bone_width = body_width // 2
            bone_height = body_height
            bone_rect = pg.Rect(head_center[0] - arm_width - body_width, arm_y - bone_height // 2,
                                 bone_width, bone_height)
            gfxdraw.box(surface, bone_rect, CannibalColors.BONE_COLOR.value)

        else:
            raise ValueError("Unknown NPC type to draw body.")

    def _draw_head(self, surface, head_center, head_radius, color):
        """
        Draws the head of the NPC.
        """
        gfxdraw.aacircle(surface, *head_center, head_radius, color)
        gfxdraw.filled_circle(surface, *head_center, head_radius, color)


    def _draw_eyes(self, surface, head_center, eye_radius, eye_y, eye_offset, color):
        """
        Draws the eyes of the NPC.
        """
        for eye_x in [head_center[0] - eye_offset, head_center[0] + eye_offset]:
            gfxdraw.aacircle(surface, eye_x, eye_y, eye_radius, color)
            gfxdraw.filled_circle(surface, eye_x, eye_y, eye_radius, color)


    def _draw_arms(self, surface, head_center, body_width, body_height, arm_y, color):
        """
        Draws the arms of the NPC.
        """
        gfxdraw.box(surface, pg.Rect([
            head_center[0] - body_width // 2 - body_height // 2, arm_y,
            body_height // 2 * 2 + body_width, body_width // 2
        ]), color)

    def _draw_body(self, surface, head_center, head_radius, body_width, body_height, color):
        """
        Draws the body of the NPC.
        """
        body_rect = pg.Rect(head_center[0] - body_width // 2, head_center[1] + head_radius,
                            body_width, body_height)
        gfxdraw.box(surface, body_rect, color)


    def _draw_legs(self, surface, head_center, head_radius, body_width, body_height, leg_width, leg_height, color):
        """
        Draws the legs of the NPC.
        """
        gfxdraw.box(surface, pg.Rect(
            head_center[0] - (body_width // 2 + body_width // 4), head_center[1] + head_radius + body_height,
            body_width // 2, leg_height
        ), color)
        gfxdraw.box(surface, pg.Rect(
            head_center[0] + body_width // 2 - body_width // 4, head_center[1] + head_radius + body_height,
            body_width // 2, leg_height
        ), color)

    def __str__(self):
        return f"NPC(type={self.npc_type}, position={self.rect.topleft}, size={self.dimensions})"

    def __repr__(self):
        return f"<NPC type={self.npc_type} at {self.rect.topleft}>"