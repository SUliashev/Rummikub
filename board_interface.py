import pygame
from chip import Chip
from chip_validator import ChipValidator
from chip_tracker import ChipTracker  # Import the ChipTracker class

class BoardInterface:
    chip_image = pygame.image.load("chips/red_1_1.png")  # Load a sample chip image
    chip_width = chip_image.get_width()
    chip_height = chip_image.get_height()

    def __init__(self, window, chip_tracker):
        self.window = window
        self.chip_tracker = chip_tracker  # Use ChipTracker for chip management
        self.board_slots = {}  # A dictionary to store slot positions for rendering
        self.hovering_slot = None  # The slot currently being hovered over
        self.hovering_slot_valid = True
        self.dragged_chip = None
        self.dragged_chip_starting_position = None
        self.chips = []  # All chips on the board

        self.create_coordinates()

    def create_coordinates(self):
        """
        Create visual coordinates for the slots.
        """
        for row in range(5):
            for col in range(29):
                x = BoardInterface.chip_width * col
                y = BoardInterface.chip_height * row * 2
                self.board_slots[(row, col)] = (x, y)  # Store the slot's visual position


    def draw_lines(self):
        """
        Draw the grid lines for the slots.
        """
        for (row, col), (x, y) in self.board_slots.items():
            pygame.draw.rect(self.window, (255, 255, 255), (x, y, BoardInterface.chip_width, BoardInterface.chip_height), 2)

    def show_hovering_slot(self):
        """
        Highlight the slot currently being hovered over.
        """
        if self.hovering_slot_valid == True:
            color = (0, 255, 0) #green
        else:
            color = (255, 0, 0) #red
        if self.hovering_slot:
            row, col = self.hovering_slot
            x, y = self.board_slots[(row, col)]
            pygame.draw.rect(self.window, color, (x, y, BoardInterface.chip_width, BoardInterface.chip_height), 7)
            self.hovering_slot = (row, col)


    def pick_up_chip(self, event):

        mouse_pos = pygame.mouse.get_pos()  # Store the mouse position once

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is clicking on any chip
            for chip in self.chips:
                if chip.x_line[0] <= mouse_pos[0] <= chip.x_line[1] and chip.y_line[0] <= mouse_pos[1] <= chip.y_line[1]:
                    self.dragged_chip = chip 
                    self.dragged_chip_starting_position = chip.x , chip.y # Set the chip being dragged
                    if chip in self.chip_tracker.get_all_chips().values():
                        self.chip_tracker.remove_chip(chip, chip.row, chip.col)
                    break

    def drag_chip(self, event, validate_func=None):
        """
        Handle dragging of chips.
        """
        mouse_pos = pygame.mouse.get_pos()  # Store the mouse position once

        if self.dragged_chip is not None and event.type == pygame.MOUSEMOTION:
            # Update the position of the dragged chip
            self.dragged_chip.x = mouse_pos[0] - self.dragged_chip.width / 2
            self.dragged_chip.y = mouse_pos[1] - self.dragged_chip.height / 2
            self.dragged_chip.update_boundaries()

            slot = self.choose_next_slot()
            self.hovering_slot = slot
            if slot and validate_func:
                row, col = slot
                # Call the GameController's validation function
                self.hovering_slot_valid = validate_func(self.dragged_chip, row, col)
            else:
                self.hovering_slot_valid = True  # Or False if you want no slot to be red by default
    
    def choose_next_slot(self, snap_range=60):
        """
        Choose the nearest empty slot for the dragged chip within snap_range.
        If the closest slot is occupied, select the next closest empty slot.
        Returns (row, col) if a slot is close enough and empty, else None.
        """
        if not self.dragged_chip:
            return None

        chip_center_x = self.dragged_chip.x + self.dragged_chip.width / 2
        chip_center_y = self.dragged_chip.y + self.dragged_chip.height / 2

        # List of (distance, (row, col)) for all slots within snap_range
        slot_distances = []
        for (row, col), (slot_x, slot_y) in self.board_slots.items():
            slot_center_x = slot_x + BoardInterface.chip_width / 2
            slot_center_y = slot_y + BoardInterface.chip_height / 2
            distance = ((chip_center_x - slot_center_x) ** 2 + (chip_center_y - slot_center_y) ** 2) ** 0.5
            if distance <= snap_range:
                slot_distances.append((distance, (row, col)))

        # Sort slots by distance
        slot_distances.sort(key=lambda x: x[0])

        # Return the closest empty slot, if any
        for _, (row, col) in slot_distances:
            if self.chip_tracker.get_chip(row, col) is None:
                self.hovering_slot = (row, col)
                return (row, col)

        # If all are occupied or none in range, return None
        return None

    def snap_chip_to_slot(self, nearest_slot=None):
        """
        Snap the dragged chip to the nearest slot.
        """

        # Snap the chip to the nearest slot if it's empty
        if nearest_slot:
            row, col = nearest_slot
            if self.chip_tracker.get_chip(row, col) is None:  # Check if the slot is empty
                self.dragged_chip.x, self.dragged_chip.y = self.board_slots[(row, col)]
                self.dragged_chip.update_boundaries()
                # self.chip_tracker.place_chip(self.dragged_chip, row, col)

        chip_placed = self.dragged_chip

        # Reset the dragged chip after snapping
        self.dragged_chip = None
        self.hovering_slot = None

        return chip_placed, nearest_slot

    def reset_dragged_chip(self, chip=None):
        """
        Reset the dragged chip to its original position.
        """
        if chip is None:
            chip = self.dragged_chip
        if chip and self.dragged_chip_starting_position:
            chip.x, chip.y = self.dragged_chip_starting_position
            chip.update_boundaries()
            self.dragged_chip = None
            self.hovering_slot = None
            self.dragged_chip_starting_position = None

            
    def draw(self):
        """
        Draw the board and chips.
        """
        self.window.fill((0, 0, 0))  # Clear the screen
        self.draw_lines()
        self.show_hovering_slot()
        for chip in self.chips:
            self.window.blit(chip.sprite, (chip.x, chip.y))


