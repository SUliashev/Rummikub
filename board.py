import pygame
from chip import Chip
from game_logic import GameLogic
from chip_tracker import ChipTracker  # Import the ChipTracker class

class Board:
    chip_image = pygame.image.load("chips/red_1_1.png")  # Load a sample chip image
    chip_width = chip_image.get_width()
    chip_height = chip_image.get_height()

    def __init__(self, window, chip_tracker):
        self.window = window
        self.chip_tracker = chip_tracker  # Use ChipTracker for chip management
        self.slots = {}  # A dictionary to store slot positions for rendering
        self.is_dragging = False
        self.chips = []  # All chips on the board

        self.create_coordinates()

    def create_coordinates(self):
        """
        Create visual coordinates for the slots.
        """
        for row in range(5):
            for col in range(29):
                x = Board.chip_width * col
                y = Board.chip_height * row * 2
                self.slots[(row, col)] = (x, y)  # Store the slot's visual position

    def draw_lines(self):
        """
        Draw the grid lines for the slots.
        """
        for (row, col), (x, y) in self.slots.items():
            pygame.draw.rect(self.window, (255, 255, 255), (x, y, Board.chip_width, Board.chip_height), 2)

    def drag(self, event):
        """
        Handle dragging of chips.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for chip in self.chips:
                if chip.x_line[0] <= mouse_pos[0] <= chip.x_line[1] and chip.y_line[0] <= mouse_pos[1] <= chip.y_line[1]:
                    self.is_dragging = chip  # Set the chip being dragged
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False

    def drag_to_slot(self):
        """
        Snap the dragged chip to the nearest slot.
        """
        if self.is_dragging and isinstance(self.is_dragging, Chip):
            # Update chip position while dragging
            mouse_pos = pygame.mouse.get_pos()
            self.is_dragging.x = mouse_pos[0] - self.is_dragging.width / 2
            self.is_dragging.y = mouse_pos[1] - self.is_dragging.height / 2
            self.is_dragging.update_boundaries()
        else:
            if self.is_dragging:
                # Snap chip to the nearest slot when dragging stops
                nearest_slot = None
                min_distance = float('inf')

                for (row, col), (slot_x, slot_y) in self.slots.items():
                    distance = (self.is_dragging.x - slot_x) ** 2 + (self.is_dragging.y - slot_y) ** 2

                    if distance < min_distance:
                        min_distance = distance
                        nearest_slot = (row, col)

                if nearest_slot:
                    row, col = nearest_slot
                    if self.chip_tracker.get_chip(row, col) is None:  # Check if the slot is empty
                        self.chip_tracker.place_chip(self.is_dragging, row, col)  # Place chip logically
                        self.is_dragging.x, self.is_dragging.y = self.slots[(row, col)]  # Snap visually
                        self.is_dragging.update_boundaries()
                    self.is_dragging = False

    def draw(self):
        """
        Draw the board and chips.
        """
        self.window.fill((0, 0, 0))  # Clear the screen
        self.draw_lines()
        for chip in self.chips:
            self.window.blit(chip.sprite, (chip.x, chip.y))


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

            board.drag(event)  # Handle dragging events

        window.fill((0, 0, 0))  # Clear the screen
        board.draw()  # Draw the board and chips
        board.drag_to_slot()  # Handle snapping logic for chips

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit the frame rate

if __name__ == "__main__":
    main()


