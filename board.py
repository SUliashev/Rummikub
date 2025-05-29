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
        """
        Handle dragging of chips.
        """
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


    def snap_chip_to_slot(self):
        """
        Snap the dragged chip to the nearest slot.
        """
        if self.dragged_chip:
            nearest_slot = None
            min_distance = float('inf')

            # Find the nearest slot
            chip_center_x = self.dragged_chip.x + self.dragged_chip.width / 2
            chip_center_y = self.dragged_chip.y + self.dragged_chip.height / 2

            for (row, col), (slot_x, slot_y) in self.board_slots.items():
                distance = ((chip_center_x - slot_x) ** 2 + (chip_center_y - slot_y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_slot = (row, col)

            # Snap the chip to the nearest slot if it's empty
            if nearest_slot:
                row, col = nearest_slot
                if self.chip_tracker.get_chip(row, col) is None:  # Check if the slot is empty
                    self.dragged_chip.x, self.dragged_chip.y = self.board_slots[(row, col)]
                    self.dragged_chip.update_boundaries()
                    self.chip_tracker.place_chip(self.dragged_chip, row, col)

            chip_placed = self.dragged_chip

            # Reset the dragged chip after snapping
            self.dragged_chip = None

            return chip_placed, nearest_slot
 
            
    def draw(self):
        """
        Draw the board and chips.
        """
        self.window.fill((0, 0, 0))  # Clear the screen
        self.draw_lines()
        for chip in self.chips:
            self.window.blit(chip.sprite, (chip.x, chip.y))


