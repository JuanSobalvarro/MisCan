import pygame as pg
from src import settings
from src.entities.map import Map
from src.entities.boat import Boat
from src.entities.npc import NPC, NPCType
from src.entities.ui.reset_button import ResetButton
from src.entities.ui.back_button import BackButton
from src.entities.ui.move_button import MoveButton
from src.entities.ui.objective_sprite import ObjectiveSprite
from src.entities.state import State
from src.enums import Shores, NPCType


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(settings.DIMENSIONS)
        pg.display.set_caption("Missionaries and Cannibals")
        self.clock = pg.time.Clock()
        self.running = True
        self.fps = settings.FPS

        # Groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.npc_sprites = pg.sprite.Group()

        self.map = self.create_map()
        self.boat = self.create_boat()
        self.reset_button = ResetButton((10, 10), (120, 40), "Reset", self.reset_game)
        self.objective_sprite = ObjectiveSprite((settings.DIMENSIONS[0] - 160, 10), (150, 100), self.objective_callback, self.map)
        self.move_button = MoveButton((10, 60), (120, 40), "Move", self.move_boat)
        # self.back_button = BackButton((140, 10), (120, 40), "Back", self.go_back)

        self.current_state = State(3, 3, ((0, 3), (3, 0)), Shores.LEFT)
        self.state_history = [self.current_state]

        self.reset_game(init=True)

    def reset_game(self, init=False):
        width, height = settings.DIMENSIONS
        self.all_sprites.empty()
        self.npc_sprites.empty()

        self.boat.reset_boat()

        # Add map and boat
        self.all_sprites.add(self.map, layer=0)
        self.all_sprites.add(self.boat, layer=1)

        # Add NPCs to the left bank
        npc_size = (height // 7, width // 10)
        for i in range(3):
            mis_w_l = width // 15
            mis_w_r = width - width // 15
            can_w_l = width // 6
            can_w_r = width - width // 6
            mis_h = height // 5 * (1 + i)
            can_h = height // 5 * (1 + i) + height // 10

            missionary = NPC((mis_w_r, mis_h), (mis_w_l, mis_h), npc_size, NPCType.MISSIONARY, Shores.LEFT, self.screen)
            cannibal = NPC((can_w_r, can_h), (can_w_l, can_h), npc_size, NPCType.CANNIBAL, Shores.LEFT, self.screen)
            self.all_sprites.add(missionary, layer=2)
            self.all_sprites.add(cannibal, layer=2)
            self.npc_sprites.add(missionary, cannibal)

        # UI
        self.all_sprites.add(self.reset_button, layer=5)
        self.all_sprites.add(self.objective_sprite, layer=5)
        self.all_sprites.add(self.move_button, layer=5)
        # self.all_sprites.add(self.back_button, layer=5)

        if not init:
            print("Game reset!")

    def objective_callback(self, objective_sprite):
        if objective_sprite.is_expanded():
            objective_sprite.unexpand_on_parent()
        else:
            objective_sprite.expand_on_parent()

    def move_boat(self):

        if not self.boat.move():
            print("Boat cannot move! Check if it has passengers.")
            return

        self.update_state()

        self.validate_state()

    def update_state(self):
        missionaries_left = 0
        cannibals_left = 0
        for npc in self.npc_sprites:
            if npc.shore == Shores.LEFT:
                if npc.npc_type == NPCType.MISSIONARY:
                    missionaries_left += 1
                elif npc.npc_type == NPCType.CANNIBAL:
                    cannibals_left += 1
            # else:
            #     raise ValueError("NPC shore is not defined correctly.")

        self.current_state.update_state(missionaries_left, cannibals_left, self.boat.current_shore)

    def validate_state(self):
        print(f"Validating state: {self.current_state}")
        if not self.current_state.is_valid():
            print("Invalid state! Missionaries killed.")
            self.reset_game()
        elif self.current_state.is_objective():
            print("Objective achieved! You win!")
            self.reset_game()
        else:
            self.state_history.append(self.current_state)

    def create_map(self):
        return Map(
            size=settings.DIMENSIONS,
            land_color=(0, 128, 0),
            water_color=(0, 0, 255),
            shore_color=(139, 69, 19),
            river_width=settings.DIMENSIONS[0] // 3,
            wavy_frequency=100,
            wavy_amplitude=10,
            shore_width=20
        )

    def create_boat(self):
        W, H = settings.DIMENSIONS
        return Boat(
            left_pos=(W // 3 - W // 20, H // 2 - H // 20),
            right_pos=(W * 2 // 3 - W // 20, H // 2 - H // 20),
            start_pos=Shores.LEFT,
            dimensions=(W // 7, H // 7)
        )

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        pg.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.reset_button.rect.collidepoint(event.pos):
                        self.reset_button.on_click()
                    elif self.objective_sprite.rect.collidepoint(event.pos):
                        self.objective_sprite.on_click()
                    elif self.move_button.rect.collidepoint(event.pos):
                        self.move_button.on_click()
                    npc = self._get_clicked_npc(event.pos)
                    if npc:
                        self._handle_npc_click(npc)

    def _get_clicked_npc(self, pos):
        for npc in self.npc_sprites:
            if npc.rect.collidepoint(pos):
                return npc
        return None

    def _handle_npc_click(self, npc_sprite):
        # Remove NPC from boat if clicked while onboard
        if npc_sprite in self.boat.passengers:
            self.boat.remove_passenger(npc_sprite)
            return

        # Attempt to board NPC if boat has space and NPC on same shore
        if not self.boat.add_passenger(npc_sprite):
            print("Error adding passenger to boat. Check if NPC is on the same shore as the boat.")
            print(f"State: {self.current_state}")
            return

    def _position_npcs_on_boat(self):
        for idx, passenger in enumerate(self.boat.passengers):
            offset_x = -15 + idx * 30  # spread passengers on boat
            passenger.rect.midbottom = (self.boat.rect.centerx + offset_x, self.boat.rect.top)

    def update(self):
        self.all_sprites.update()
        # print("Current State:", self.current_state)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_sprites.draw(self.screen)
        pg.display.flip()
