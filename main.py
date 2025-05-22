import pygame
from board import Board

def main():
    pygame.init()
    window = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    # Initialize the board and pass the window
    board = Board(window)

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

