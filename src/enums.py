from enum import Enum


class Shores(Enum):
    LEFT = "left"
    RIGHT = "right"


class NPCType(Enum):
    MISSIONARY = 0
    CANNIBAL = 1


class MissionaryColors(Enum):
    SKIN_TONE = (230, 190, 160)  # skin tone
    EYE_COLOR = (0, 0, 0)  # black
    SHIRT_COLOR = (10, 10, 10)
    PANTS_COLOR = (40, 60, 140)  # blue pants
    BIBLE_COLOR = (111, 66, 36)
    CRUX_COLOR = (200, 200, 200)


class CannibalColors(Enum):
    SKIN_TONE = (255, 130, 100)  # darker skin tone
    EYE_COLOR = (0, 150, 0)
    MOUTH_COLOR = (180, 0, 0)  # red for danger
    PANTS_COLOR = (100, 50, 0)  # brown pants
    BONE_COLOR = (250, 250, 250)  # white bone color