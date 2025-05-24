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
        self.board_slots = {}  # A dictionary to store slot positions for rendering
        self.dragged_chip = None
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
                self.board_slots[(row, col)] = (x, y)  # Store the slot's visual position


    def draw_lines(self):
        """
        Draw the grid lines for the slots.
        """
        for (row, col), (x, y) in self.board_slots.items():
            pygame.draw.rect(self.window, (255, 255, 255), (x, y, Board.chip_width, Board.chip_height), 2)

    def drag(self, event):
        mouse_pos = pygame.mouse.get_pos()  # Store the mouse position once

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is clicking on any chip
            for chip in self.chips:
                if chip.x_line[0] <= mouse_pos[0] <= chip.x_line[1] and chip.y_line[0] <= mouse_pos[1] <= chip.y_line[1]:
                    self.dragged_chip = chip  # Set the chip being dragged
                    break

        elif self.dragged_chip is not None and event.type == pygame.MOUSEMOTION:
            # Update the position of the dragged chip
            self.dragged_chip.x = mouse_pos[0] - self.dragged_chip.width / 2
            self.dragged_chip.y = mouse_pos[1] - self.dragged_chip.height / 2
            self.dragged_chip.update_boundaries()

        elif event.type == pygame.MOUSEBUTTONUP and self.dragged_chip is not None:
            # Handle snapping the chip to the nearest slot
            nearest_slot = None
            min_distance = float('inf')

            # Define a bounding box around the dragged chip
            search_radius = max(Board.chip_width, Board.chip_height) * 2
            chip_center_x = self.dragged_chip.x + self.dragged_chip.width / 2
            chip_center_y = self.dragged_chip.y + self.dragged_chip.height / 2

            # Find the nearest slot within the search radius
            for (row, col), (slot_x, slot_y) in self.board_slots.items():
                if abs(slot_x - chip_center_x) <= search_radius and abs(slot_y - chip_center_y) <= search_radius:
                    distance = ((chip_center_x - slot_x) ** 2 + (chip_center_y - slot_y) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        nearest_slot = (row, col)

            # Log the nearest slot and distance for debugging purposes
            import logging
            logging.debug(f"Nearest slot: {nearest_slot}, Distance: {min_distance}")

            # Snap the chip to the nearest slot if it's empty
            if nearest_slot:
                row, col = nearest_slot  # Unpack the nearest slot
                if self.chip_tracker.get_chip(row, col) is None:  # Check if the slot is empty
                    self.dragged_chip.x, self.dragged_chip.y = self.board_slots[(row, col)]
                    self.dragged_chip.update_boundaries()
                    self.chip_tracker.place_chip(self.dragged_chip, row, col)

            # Reset the dragged chip after snapping
            self.dragged_chip = None

    # def drag_to_slot(self):
    #     if self.is_dragging and isinstance(self.is_dragging, Chip):
    #         # Update chip position while dragging

    #     else:
            
    def draw(self):
        """
        Draw the board and chips.
        """
        self.window.fill((0, 0, 0))  # Clear the screen
        self.draw_lines()
        for chip in self.chips:
            self.window.blit(chip.sprite, (chip.x, chip.y))


# def main():
#     pygame.init()
#     window = pygame.display.set_mode((1920, 1080))
#     clock = pygame.time.Clock()

#     # Initialize the board and pass the window
#     chip_tracker = ChipTracker()
#     board = Board(window, chip_tracker)

#     # Add one chip for experimentation
#     chip = Chip(100, 100, "chips/red_1_1.png")  # Create a chip at position (100, 100)
#     board.chips.append(chip)  # Add the chip to the board's chip list


