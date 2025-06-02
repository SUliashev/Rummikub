import pygame
from board import BoardInterface
from chip_tracker import ChipTracker
from chip_validator import ChipValidator
from chip import Chip

class GameController:
    def __init__(self, window):
        self.window = window
        self.chip_tracker = ChipTracker()
        self.board = BoardInterface(window, self.chip_tracker)
        self.game_logic = ChipValidator(self.chip_tracker)
        self.current_player = "Player 1"  # Example: Start with Player 1

        # Add testing chips
        self.add_testing_chips()

    def add_testing_chips(self):
        """
        Add testing chips to the board and chip tracker for experimentation.
        """
        colors = ["red", "black"]  # Colors for the chips
        numbers = range(1, 8)  # Numbers from 1 to 7
        y_position = 800  # Starting y-position for chips

        for color in colors:
            for number in numbers:
                second = 0 if color == "red" else 7 * 70
                x_position = (number - 1) * 70 + second  # Space chips horizontally
                image_path = f"chips/{color}_{number}_1.png"  # Example sprite path
                chip = Chip(x_position, y_position, image_path, color=color, number=number)

                # Add chips to the board's chip list fors rendering
                self.board.chips.append(chip)

                # # Place chips in the chip tracker (optional: specify row/col)
                # row, col = 0 if color == "red" else 1, number - 1  # Red chips in row 0, black chips in row 1
                # self.chip_tracker.place_chip(chip, row, col)

    def handle_event(self, event):
        """
        Handle a single pygame event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.board.pick_up_chip(event)

        elif event.type == pygame.MOUSEMOTION and self.board.dragged_chip is not None:
            self.board.drag_chip(event, validate_func=self.validate_chip_placement)
            self.board.show_hovering_slot
            self.board.choose_next_slot()

        elif event.type == pygame.MOUSEBUTTONUP:
            # Handle snapping logic
            snapped_chip, snapped_slot = self.board.snap_chip_to_slot(self.board.choose_next_slot())
            if snapped_chip and snapped_slot:
                row, col = snapped_slot
                self.place_chip_and_validate(snapped_chip, row, col)

    def validate_chip_placement(self, chip, row, col):
        # Temporarily place the chip in the validation slot
        self.chip_tracker.validate_chip(chip, row, col)
        is_valid = self.game_logic.validate_combination(row, col)
        self.chip_tracker.validation_slots[(row, col)] = None
        return is_valid

    def place_chip_and_validate(self, chip, row, col):
        """
        Place a chip and validate the move.
        """
        
        try:
            self.chip_tracker.place_chip(chip, row, col)
            if len(self.game_logic.get_chips_in_combination(row, col)) > 2:
                if not self.game_logic.validate_combination(row, col):        # To Do LATER
                    print(f"Invalid combination for chip at ({row}, {col})")
                    # Handle invalid move (e.g., return chip to original position)
                else:
                    print(f"Valid combination for chip at ({row}, {col})")
                    self.switch_turn()
        except ValueError as e:
            print("place_chip_and_validate does not work")

    def switch_turn(self):
        """
        Switch to the next player's turn.
        """
        self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"
        print(f"It's now {self.current_player}'s turn!")

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