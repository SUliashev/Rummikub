import pygame
from board import Board
from chip_tracker import ChipTracker
from chip import Chip  # Import the Chip class

def main():
    pygame.init()
    window = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    # Initialize the board and pass the window
    chip_tracker = ChipTracker()
    board = Board(window, chip_tracker)

    # Add one chip for experimentation
    chip = Chip(100, 100, "chips/red_1_1.png")  # Create a chip at position (100, 100)
    board.chips.append(chip)  # Add the chip to the board's chip list

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            board.drag(event)

        window.fill((0, 0, 0))  # Clear the screen
        board.draw()  # Draw the board and chips
        board.drag_to_slot()  # Handle dragging logic

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit the frame rate

if __name__ == "__main__":
    main()

