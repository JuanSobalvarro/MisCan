import pygame as pg
from src import settings
from src.entities.map import Map
from src.entities.boat import Boat
from src.entities.npc import NPC, NPCType
from src.entities.ui.reset_button import ResetButton
from src.entities.ui.back_button import BackButton
from src.entities.ui.move_button import MoveButton
from src.entities.ui.solve_button import SolveButton
from src.entities.ui.objective_sprite import ObjectiveSprite
from src.entities.ui.counter_frame import CounterFrame
from src.entities.ui.alert import Alert
from src.entities.state import State
from src.enums import Shores, NPCType
from src.solver import Solver
import copy


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(settings.DIMENSIONS)
        pg.display.set_caption("Missionaries and Cannibals")
        self.clock = pg.time.Clock()
        self.running = True
        self.auto_solving = False
        self.fps = settings.FPS
        self.counter = CounterFrame((100, 50), (0, settings.DIMENSIONS[1] - 50), self.screen)
        self.objective_state = ((0, 0), (3, 3))

        self.current_state = State(3, 3, self.objective_state, Shores.LEFT, self.counter.counter)
        self.state_history = [self.current_state]

        # Groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.npc_sprites = pg.sprite.Group()

        self.map = self.create_map()
        self.boat = self.create_boat()
        self.reset_button = ResetButton((10, 10), (120, 40), "Reset", self.reset_game)
        self.move_button = MoveButton((10, 60), (120, 40), "Move", self.move_boat)
        self.back_button = BackButton((140, 10), (120, 40), "Back", self.go_back)
        self.solve_button = SolveButton((140, 60), (120, 40), "Solve", self.solve_from_current_state)
        self.objective_sprite = ObjectiveSprite(self.current_state, (settings.DIMENSIONS[0] - 160, 10), (150, 100), self.objective_callback, self.map)

        self.good_alert = Alert((settings.DIMENSIONS[0] // 2 - settings.DIMENSIONS[0] // 10, settings.DIMENSIONS[1] // 2 - 50),
                                (settings.DIMENSIONS[0] // 5, settings.DIMENSIONS[1] // 5), (0, 255, 0), "UWUNYA", self.good_alert_callback)

        self.warning_alert = Alert((settings.DIMENSIONS[0] // 2 - settings.DIMENSIONS[0] // 10, settings.DIMENSIONS[1] // 2 - 50),
                                (settings.DIMENSIONS[0] // 5, settings.DIMENSIONS[1] // 5), (220, 120, 0), "Warning!", None)

        self.bad_alert = Alert((settings.DIMENSIONS[0] // 2 - settings.DIMENSIONS[0] // 10, settings.DIMENSIONS[1] // 2 - 50),
                                (settings.DIMENSIONS[0] // 5, settings.DIMENSIONS[1] // 5), (255, 0, 0), "Missionaries killed!", None)

        self.reset_game(init=True)

    def good_alert_callback(self):
        self.good_alert.text = f"You Win with: {self.counter.counter} moves!"

    def go_back(self):
        if len(self.state_history) == 1:
            self.warning_alert.text = f"You should move!"
            self.warning_alert.show_alert_ms(self.screen, 2000)
            return

        if len(self.state_history) == 2:
            # reset game
            self.reset_game()
            return

        # Pop the last state and set the game to that state
        print(f"States history before rollback: {self.state_history}")
        self.state_history.pop(-1)
        previous_state = self.state_history[-1]
        self.current_state = previous_state

        print("Rolling back to state:", self.current_state)

        self.roll_to_state(self.current_state)

    def solve_from_current_state(self):
        self.auto_solving = True
        states: list[State] = Solver.solve_from_state(self.current_state)

        delay_between_moves = 500  # milliseconds
        last_move_time = pg.time.get_ticks()

        current_index = 0
        solving = True

        while solving:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

            now = pg.time.get_ticks()
            if now - last_move_time >= delay_between_moves:
                if current_index < len(states):
                    self.roll_to_state(states[current_index])
                    current_index += 1
                    last_move_time = now
                else:
                    solving = False
                    self.validate_state(self.current_state)
                    self.auto_solving = False

    def roll_to_state(self, state: State):
        # Roll back counter
        self.counter.set_counter(state.counter)

        # Roll back boat
        self.boat.current_shore = state.boat_position
        self.boat.set_position(state.boat_position)

        # Roll back NPCs
        missionaries_left = state.missionaries_left
        cannibals_left = state.cannibals_left

        for npc in self.npc_sprites:
            if npc.npc_type == NPCType.MISSIONARY:
                if missionaries_left > 0:
                    npc.set_shore(Shores.LEFT)
                    missionaries_left -= 1
                else:
                    npc.set_shore(Shores.RIGHT)
            elif npc.npc_type == NPCType.CANNIBAL:
                if cannibals_left > 0:
                    npc.set_shore(Shores.LEFT)
                    cannibals_left -= 1
                else:
                    npc.set_shore(Shores.RIGHT)

        self.current_state = state



    def reset_game(self, init=False):
        width, height = settings.DIMENSIONS
        self.all_sprites.empty()
        self.npc_sprites.empty()

        self.boat.reset_boat()

        self.counter.reset()

        self.current_state = State(3, 3, self.objective_state, Shores.LEFT, self.counter.counter)
        self.state_history = [self.current_state]

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
        self.all_sprites.add(self.move_button, layer=5)
        self.all_sprites.add(self.back_button, layer=5)
        self.all_sprites.add(self.solve_button, layer=5)

        self.all_sprites.add(self.counter, layer=5)

        self.all_sprites.add(self.objective_sprite, layer=5)

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

        self.counter.increase()

        self.current_state = self.update_state()

        self.draw()

        self.validate_state(self.current_state)

    def update_state(self):
        missionaries_left = 0
        cannibals_left = 0
        for npc in self.npc_sprites:
            if npc.shore == Shores.LEFT:
                if npc.npc_type == NPCType.MISSIONARY:
                    missionaries_left += 1
                elif npc.npc_type == NPCType.CANNIBAL:
                    cannibals_left += 1

        return State(missionaries_left, cannibals_left, self.objective_state, self.boat.current_shore,
                     self.counter.counter)

    def validate_state(self, state: State):
        print(f"Validating state: {state}")
        if not state.is_valid():
            print("Invalid state! Missionaries killed.")
            self.bad_alert.show_alert_ms(self.screen, 2000)
            self.reset_game()
        elif state.is_objective():
            print(f"Objective achieved! You win!. In {self.counter.counter} moves.")
            self.good_alert.show_alert_ms(self.screen, 2000)
            self.reset_game()
        else:
            self.state_history.append(copy.deepcopy(state))

    def create_map(self):
        return Map(
            size=settings.DIMENSIONS,
            land_color=(0, 128, 0),
            water_color=(0, 0, 255),
            shore_color=(139, 69, 19),
            river_width=settings.DIMENSIONS[0] // 3,
            wavy_frequency=100,
            wavy_amplitude=10,
            shore_width=30
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
                if self.auto_solving:
                    continue
                if event.button == 1:
                    if self.reset_button.rect.collidepoint(event.pos):
                        self.reset_button.on_click()
                    elif self.objective_sprite.rect.collidepoint(event.pos):
                        self.objective_sprite.on_click()
                    elif self.move_button.rect.collidepoint(event.pos):
                        self.move_button.on_click()
                    elif self.back_button.rect.collidepoint(event.pos):
                        self.back_button.on_click()
                    elif self.solve_button.rect.collidepoint(event.pos):
                        self.solve_button.on_click()
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
