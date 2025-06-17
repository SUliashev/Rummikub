from typing import Dict
import pygame
from chip import Chip
from chip_sprite_generator import ChipSpriteGenerator
from game_ui import GameUI
from chip_tracker import ChipTracker
from board_grid import BoardGrid
from tray_grid import TrayGrid
from chip_validator import ChipValidator
from player_interaction import PlayerInteraction  
from config import Config
import random


class GameController:
    def __init__(self, sprites: Dict[str, pygame.Surface]):
        self.sprites = sprites
        self.board_grid = BoardGrid()
        self.tray_grid = TrayGrid()
        self.chip_tracker = ChipTracker(self.board_grid, self.tray_grid)
        self.generate_and_shuffle_hidden_chips()

        
        self.game_ui = GameUI( self.chip_tracker)  # Initialize GameUI with the window and chip tracker
        

        

        # self.chip_validator = ChipValidator()
        # self.player_interaction = PlayerInteraction(self.chip_tracker, self.tray, self. game_ui)  # Placeholder for player interaction logic
        # self.tray = Tray()
        # self.game_ui = GameUI(self.window, self.chip_tracker, self.chip_validator, self.tray)
        # self.current_player = "Player 1"  # Example: Start with Player 1


        # self.generate_and_shuffle_hidden_chips()
        # Add testing chips
        # self.add_testing_chips()
        
    def draw(self):
        """
        Draw the game components.
        """
        self.game_ui.draw()  # Draw the board and chips
        pygame.display.flip()  # Update the display

    def run(self):
        """
        Main game loop.
        """
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                # self.handle_event(event) #testing stage

            self.draw()
            clock.tick(60)  # Limit the frame rate

    def generate_and_shuffle_hidden_chips(self):
        colors = ["red", "blue", "orange", "black"]
        numbers = range(1, 14)
        hidden_chips = []

        for color in colors:
            for number in numbers:
                for _ in range(2):  # Two of each chip
                    chip = Chip(0, 0, self.sprites[f"{color}_{number}_1"], color=color, number=number)
                    hidden_chips.append(chip)


        random.shuffle(hidden_chips)
        self.chip_tracker.hidden = hidden_chips

    def handle_event(self, event):
        """
        Handle a single pygame event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mousebutton_dowm(event)

            
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mousemotion(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mousebutton_up()

    def handle_mousebutton_dowm(self, event):
        self.game_ui.pick_up_chip(event)
        self.game_ui.handle_draw_chip_button(self.chip_tracker)

    def handle_mousemotion(self, event):
        if self.game_ui.dragged_chip:
            self.game_ui.drag_chip(event)
            # Decide which slot logic to use based on mouse position
            if self.game_ui.is_mouse_over_tray():
                slot = self.game_ui.choose_next_tray_slot()
            else:
                slot = self.game_ui.choose_next_slot()
            if slot:
                self.validate_chip_placement(self.chip_tracker, self.game_ui.dragged_chip, *slot)
        
    def handle_mousebutton_up(self):
        # Decide which slot logic to use based on mouse position
        if self.game_ui.is_mouse_over_tray():
            tray_slot = self.game_ui.choose_next_tray_slot()
            # Optionally, validate tray placement here if needed
            snapped_chip, snapped_slot = self.game_ui.snap_chip_to_tray_slot(tray_slot)
            if snapped_chip and snapped_slot:
                self.chip_tracker.get_all_chips_in_tray()
        else:
            board_slot = self.game_ui.choose_next_slot()
            if board_slot and self.game_ui.dragged_chip:
                row, col = board_slot
                valid_placement = self.validate_chip_placement(self.chip_tracker, self.game_ui.dragged_chip, row, col)
                if valid_placement:
                    snapped_chip, snapped_slot = self.game_ui.snap_chip_to_slot(board_slot)

                    if snapped_chip and snapped_slot:
                        self.place_chip_on_board(snapped_chip, row, col)
                else:
                    self.game_ui.snap_chip_back_to_origin()
            else:
                # If not over a valid slot, snap back to origin
                self.game_ui.snap_chip_back_to_origin()

        


    def validate_chip_placement(self, chip_tracker, chip, row, col):
        # self.chip_validator.validate_chip(chip, row, col) # dont think this is needed
        is_valid = self.chip_validator.validate_combination(chip_tracker, chip, row, col)
        self.game_ui.hovering_slot_valid = is_valid
        return is_valid

    def place_chip_on_board(self, chip, row, col):
        self.chip_tracker.place_chip_in_slot(chip, row, col)
        chip.put_chip_in_slot(row, col)
        self.game_ui.dragged_chip = None

    def place_chip_in_tray(self, chip, row, col):   
        self.chip_tracker.place_chip_in_tray(chip, row, col)
        chip.put_chip_in_tray(row, col)
        self.game_ui.dragged_chip = None

    def switch_turn(self):
        """
        Switch to the next player's turn.
        """
        self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"
        print(f"It's now {self.current_player}'s turn!")



    
