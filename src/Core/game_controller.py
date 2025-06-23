from typing import Dict
import pygame
from src.Core.chip import Chip
from src.GameUI.dragging_chip import DraggingChip
from src.Core.players import Player 
from src.GameUI.game_ui import GameUI
from src.Core.chip_tracker import ChipTracker
from src.Grids.board_grid import BoardGrid
from src.Grids.tray_grid import TrayGrid
from src.Core.chip_validator import ChipValidator
from src.GameUI.player_interaction import PlayerInteraction  
import random

class GameController:
    def __init__(self, sprites: Dict[str, pygame.Surface], dispatcher):
        self.dispatcher = dispatcher
        self.subscribe_events()
        self.sprites = sprites
        self.board_grid = BoardGrid()
        self.moving_chip = DraggingChip()  

        self.players = self.create_players(2)
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]

        self.chip_tracker = ChipTracker(self.board_grid, self.players[self.current_player_index].tray_grid, self.moving_chip, self.dispatcher)
        self.generate_and_shuffle_hidden_chips()
        self.test_draw_from_hidden()  # can be removed later 
        self.chip_validator = ChipValidator(self.chip_tracker)

        self.player_interaction = PlayerInteraction(self.chip_tracker, self.chip_validator, self.dispatcher) 
        self.game_ui = GameUI(self.chip_tracker, self.chip_validator, self.current_player, self.dispatcher) 
        

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                self.player_interaction.handle_event(event) #testing stage
            

            self.draw()
            clock.tick(60)  


    def draw(self):
        self.game_ui.draw()  
        pygame.display.flip()  


    def create_players(self, number_of_players):
        players = []
        for player in range(1, number_of_players + 1):
            players.append(Player(f"Player {player}", TrayGrid()))

        return players


    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        self.chip_tracker.tray_grid = self.current_player.tray_grid
        self.game_ui.current_player = self.current_player
        print(f"Switched to {self.current_player.name}")


    def generate_and_shuffle_hidden_chips(self):
        colors = ["red", "blue", "orange", "black"]
        numbers = range(1, 14)
        hidden_chips = []

        for color in colors:
            for number in numbers:
                for _ in range(2):  # Two of each chip
                    chip = Chip(self.sprites[f"{color}_{number}_1"], color=color, number=number)
                    hidden_chips.append(chip)

        for i in range(2):
            chip = Chip(self.sprites['joker'], 'purple', None, True) 
            hidden_chips.append(chip)

        random.shuffle(hidden_chips)
        self.chip_tracker.hidden_chips = hidden_chips


    def test_draw_from_hidden(self):
        for i in range(14):
            self.chip_tracker.place_chip_in_tray_from_hidden()



    def subscribe_events(self):
        self.dispatcher.subscribe('chip_drag_start', self.on_chip_drag_start)
        self.dispatcher.subscribe('chip_drag_end', self.on_chip_drag_end)
        self.dispatcher.subscribe('button next player pressed', self.next_turn)
 

    def on_chip_drag_start(self, slot_type, slot, **kwargs):
        if slot_type == 'tray':
            if self.chip_tracker.tray_grid.slots[slot]:
                self.chip_tracker.chip_from_tray_to_dragging(slot)
                self.chip_validator.validate_dragging_chip()
                
        elif slot_type == 'board':
            if self.chip_tracker.board_grid.slots[slot]:
                self.chip_tracker.chip_from_board_to_dragging(slot)
                self.chip_validator.validate_dragging_chip()
                self.chip_validator.validate_current_state()


    def on_chip_drag_end(self, slot_type, **kwargs):
        next_slot = self.chip_tracker.hovering_slot
        if next_slot == None:
            self.chip_tracker.return_chip_to_origin_pos()
            self.chip_validator.validate_current_state()
        elif next_slot[0] == 'board':
            if self.chip_validator.slots[next_slot[1]]:
                self.chip_tracker.chip_from_dragging_to_board(next_slot[1])
                self.chip_validator.validate_current_state()
            else:
                self.chip_tracker.return_chip_to_origin_pos()
                self.chip_validator.validate_current_state()
 
        elif next_slot[0] == 'tray':
            self.chip_tracker.chip_from_dragging_to_tray(next_slot[1])
         
        else:
            print('error with releasing chip')