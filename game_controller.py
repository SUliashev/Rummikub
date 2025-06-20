from typing import Dict
import pygame
from chip import Chip
from dragging_chip import DraggingChip
from players import Player 
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
        self.moving_chip = DraggingChip()  # Placeholder for the chip being dragged
        self.chip_tracker = ChipTracker(self.board_grid, self.tray_grid, self.moving_chip)
        self.chip_validator = ChipValidator(self.chip_tracker)

        self.generate_and_shuffle_hidden_chips()
        self.test_draw_from_hidden()  # can be removed later 
        self.player_interaction = PlayerInteraction(self.chip_tracker, self.chip_validator)  # Placeholder for player interaction logic 
        self.players = [
            Player("Player 1", TrayGrid()),
            Player("Player 2", TrayGrid()),
            # Add more players as needed
        ]
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]

        self.game_ui = GameUI(self.chip_tracker, self.chip_validator)  # Initialize GameUI with the window and chip tracker
        
        # self.current_player = "Player 1"  # Example: Start with Player 1

        
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
                self.player_interaction.handle_event(event) #testing stage

            self.draw()
            clock.tick(60)  # Limit the frame rate

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
        for i in range(4):
            self.chip_tracker.place_chip_in_tray_from_hidden()



    # def switch_turn(self):
    #     """
    #     Switch to the next player's turn.
    #     """
    #     self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"
    #     print(f"It's now {self.current_player}'s turn!")



    
