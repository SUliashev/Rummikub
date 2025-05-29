import pygame
from board import Board
from chip_tracker import ChipTracker
from game_logic import GameLogic
from chip import Chip

class GameController:
    def __init__(self, window):
        self.window = window
        self.chip_tracker = ChipTracker()
        self.board = Board(window, self.chip_tracker)
        self.game_logic = GameLogic(self.chip_tracker)
        self.players = ["Player 1", "Player 2"]  # Example: Two players
        self.current_player_index = 0  # Start with Player 1
        self.chips = []  # Store all generated chips
        self.generate_chips()

    def generate_chips(self):
        """
        Generate chips with unique sprites and assign them to the board.
        """
        colors = ["red", "blue", "black", "orange"]  
        numbers = range(1, 14)  # Numbers 1 to 13
        y_position = 800  # Example starting y-position for chips

        for color in colors:
            for number in numbers:
                x_position = 100 + len(self.chips) * (Chip(0, 0, "chips/red_1_1.png").width + 10)
                image_path = f"chips/{color}_{number}_1.png"  # Example sprite path
                chip = Chip(x_position, y_position, image_path, color, number)
                self.chips.append(chip)
                self.board.chips.append(chip)  # Add chip to the board

    def switch_turn(self):
        """
        Switch to the next player's turn.
        """
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        print(f"It's now {self.players[self.current_player_index]}'s turn!")

    def handle_event(self, event):
        """
        Handle a single pygame event.
        """
        self.board.drag(event)  # Handle dragging logic

        # if event.type == pygame.MOUSEBUTTONUP:
        #     self.board.drag_to_slot()  # Handle snapping logic
        #     self.switch_turn()  # Switch turns after a move

    def draw(self):
        """
        Draw the game components.
        """
        self.window.fill((0, 0, 0))  # Clear the screen
        self.board.draw()  # Draw the board and chips
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
                self.handle_event(event)

            self.draw()
            clock.tick(60)  # Limit the frame rate

    def place_chip_and_validate(self, chip, row, col):
        """
        Place a chip and validate the move.
        """
        try:
            self.chip_tracker.place_chip(chip, row, col)
            if not self.game_logic.validate_combination(row, col):
                print(f"Invalid combination for chip at ({row}, {col})")
                # Handle invalid move (e.g., return chip to original position)
            else:
                print(f"Valid combination for chip at ({row}, {col})")
        except ValueError as e:
            print(e)