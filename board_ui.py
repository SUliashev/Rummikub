import pygame
from chip import Chip
from chip_validator import ChipValidator
from chip_tracker import ChipTracker  # Import the ChipTracker class
from tray import Tray

class BoardInterface:
    chip_image = pygame.image.load("chips/red_1_1.png")  # Load a sample chip image
    chip_width = chip_image.get_width()
    chip_height = chip_image.get_height()

    def __init__(self, window, chip_tracker, chip_validator, tray):
        self.window = window
        self.chip_tracker = chip_tracker  # Use ChipTracker for chip management
        self.board_slots = {}  # A dictionary to store slot positions for rendering
        self.tray_slots = {}
        self.tray = tray
        self.chip_validator = chip_validator  # Initialize the chip validator
        self.hovering_tray_slot = None
        self.hovering_slot = None  # The slot currently being hovered over
        self.hovering_slot_valid = True
        self.dragged_chip = None
        self.dragged_chip_starting_position = None
        self.chips = []  # All chips on the board

        self.create_coordinates()
        self.create_tray_coordinates()

    def update_chip_coordinates(self):
        """
        Update the coordinates of all chips on the board.
        This should be called after placing or moving chips.
        """
        for chip in self.chips:
            if chip.state == Chip.board:
                chip.x, chip.y = self.board_slots[(chip.row, chip.col)]
            elif chip.state == Chip.tray:
                chip.x, chip.y = self.tray_slots[(chip.tray_row, chip.tray_col)]
            chip.update_boundaries()


    def is_mouse_over_tray(self):
        """
        Check if the mouse is currently over the tray area.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tray_rect = pygame.Rect(self.tray.x, self.tray.y, self.tray.width, self.tray.height)
        return tray_rect.collidepoint(mouse_x, mouse_y)
    
    def pick_up_chip(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_mouse_over_tray():
                # Check tray chips only
                for chip in self.chip_tracker.tray_slots.values():
                    if chip and chip.x_line[0] <= mouse_pos[0] <= chip.x_line[1] and chip.y_line[0] <= mouse_pos[1] <= chip.y_line[1]:
                        self.dragged_chip = chip
                        self.dragged_chip_starting_position = chip.tray_row, chip.tray_col
                        self.chip_tracker.remove_chip_from_tray(chip, chip.tray_row, chip.tray_col)
                        print(f"Picked up chip {chip} from tray")
                        break
            else:
                # Check board chips only
                for chip in self.chips:
                    if chip.x_line[0] <= mouse_pos[0] <= chip.x_line[1] and chip.y_line[0] <= mouse_pos[1] <= chip.y_line[1]:
                        self.dragged_chip = chip
                        self.dragged_chip_starting_position = chip.row, chip.col
                        print(self.dragged_chip_starting_position)
                        self.chip_tracker.remove_chip(chip, chip.row, chip.col)
                        break
    

    def drag_chip(self, event, validate_func=None):
        """
        Handle dragging of chips.
        """
        mouse_pos = pygame.mouse.get_pos()  # Store the mouse position once

        self.dragged_chip.x = mouse_pos[0] - self.dragged_chip.width / 2
        self.dragged_chip.y = mouse_pos[1] - self.dragged_chip.height / 2
        self.dragged_chip.update_boundaries()

    def choose_next_slot(self, snap_range=60):
        """
        Choose the nearest empty slot for the dragged chip within snap_range.
        If the closest slot is occupied, select the next closest empty slot.
        Returns (row, col) if a slot is close enough and empty, else None.
        """
        if not self.dragged_chip:
            self.hovering_slot = None
            return None

        if self.dragged_chip.y < self.window.get_height() - (BoardInterface.chip_height / 2) - self.tray.get_height():
            chip_center_x = self.dragged_chip.x + self.dragged_chip.width / 2
            chip_center_y = self.dragged_chip.y + self.dragged_chip.height / 2

            slot_distances = []
            for (row, col), (slot_x, slot_y) in self.board_slots.items():
                slot_center_x = slot_x + BoardInterface.chip_width / 2
                slot_center_y = slot_y + BoardInterface.chip_height / 2
                distance = ((chip_center_x - slot_center_x) ** 2 + (chip_center_y - slot_center_y) ** 2) ** 0.5
                if distance <= snap_range:
                    slot_distances.append((distance, (row, col)))

            slot_distances.sort(key=lambda x: x[0])
            for _, (row, col) in slot_distances:
                if self.chip_tracker.get_chip(row, col) is None:
                    self.hovering_slot = (row, col)
                    self.hovering_tray_slot = None
                    return (row, col)

    # If no slot is in range, clear hovering
        self.hovering_slot = None
        return None
    
    def choose_next_tray_slot(self, snap_range=60):
        """
        Choose the nearest empty tray slot for the dragged chip within snap_range.
        Returns (row, col) if a slot is close enough and empty, else None.
        """
        if not self.dragged_chip:
            self.hovering_tray_slot = None
            return None

        if self.dragged_chip.y >= self.window.get_height() - (BoardInterface.chip_height / 2) - self.tray.get_height():

            chip_center_x = self.dragged_chip.x + self.dragged_chip.width / 2
            chip_center_y = self.dragged_chip.y + self.dragged_chip.height / 2

            slot_distances = []
            for (row, col), (slot_x, slot_y) in self.tray_slots.items():
                slot_center_x = slot_x + BoardInterface.chip_width / 2
                slot_center_y = slot_y + BoardInterface.chip_height / 2
                distance = ((chip_center_x - slot_center_x) ** 2 + (chip_center_y - slot_center_y) ** 2) ** 0.5
                # Check if tray slot is empty and within snap range
                if distance <= snap_range and self.chip_tracker.tray_slots.get((row, col)) is None:
                    slot_distances.append((distance, (row, col)))

            slot_distances.sort(key=lambda x: x[0])
            if slot_distances:
                self.hovering_tray_slot = slot_distances[0][1]
                self.hovering_slot = None
                return slot_distances[0][1]

    # If no tray slot is in range, clear hovering
        self.hovering_tray_slot = None
        return None
       

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

    def show_hovering_tray_slot(self):
        """
        Highlight the tray slot currently being hovered over.
        If valid is True, use green; else use red.
        """
        if self.hovering_tray_slot:
            row, col = self.hovering_tray_slot
            x, y = self.tray_slots[(row, col)]
            color = (0, 255, 0) 
            pygame.draw.rect(
                self.window,
                color,
                (x, y, BoardInterface.chip_width, BoardInterface.chip_height),
                5,  # thickness
                border_radius=12
            )

    def handle_chip_snapping(self):
        """
        Handle the snapping of the chip to the nearest slot or tray position.
        This method should be called after dragging a chip.
        """
        if self.is_mouse_over_tray():
            tray_slot = self.choose_next_tray_slot()
            # Snap to tray slot if available
            if tray_slot:
                # Place chip in tray slot, update chip position, etc.
                chip_placed, _ = self.snap_chip_to_tray_slot(tray_slot)
                if chip_placed:
                    self.place_chip_in_tray(chip_placed)
        else:
            board_slot = self.choose_next_slot()
            # Snap to board slot if available
            if board_slot:
                # Place chip in board slot, update chip position, etc.
                chip_placed, _ = self.snap_chip_to_slot(board_slot)
                if chip_placed:
                    # Additional logic for placing chip on board if needed
                    pass

    def snap_chip_to_slot(self, nearest_slot=None):
        """
        Snap the dragged chip to the nearest slot.
        """

        # Snap the chip to the nearest slot if it's empty
        if nearest_slot:
            row, col = nearest_slot
            if self.chip_tracker.get_chip(row, col) is None:  # Check if the slot is empty
                self.dragged_chip.x, self.dragged_chip.y = self.board_slots[(row, col)]
                self.dragged_chip.row = row
                self.dragged_chip.col = col
                self.dragged_chip.update_boundaries()
                # self.chip_tracker.place_chip(self.dragged_chip, row, col)

        chip_placed = self.dragged_chip

        # Reset the dragged chip after snapping
        self.dragged_chip = None
        self.hovering_slot = None

        return chip_placed, nearest_slot
    

    def snap_chip_to_tray_slot(self, tray_slot):
        """
        Snap the dragged chip to the given tray slot (row, col).
        Returns (chip, (row, col)) if successful, else (None, None).
        """
        if tray_slot:
            row, col = tray_slot
            if self.chip_tracker.tray_slots.get((row, col)) is None:
                # Move chip to tray slot
    
                self.chip_tracker.tray_slots[(row, col)] = self.dragged_chip
                self.dragged_chip.tray_row = row
                self.dragged_chip.tray_col = col
                self.dragged_chip.state = Chip.tray
                self.dragged_chip.x, self.dragged_chip.y = self.tray_slots[(row, col)]
                self.dragged_chip.update_boundaries()
                chip = self.dragged_chip
                self.dragged_chip = None
                return chip, (row, col)
        return None, None


    def snap_chip_back_to_origin(self):
        """
        Snap the dragged chip back to its original position if not placed in a valid slot or combination is invalid.
        """
        if self.dragged_chip and self.dragged_chip_starting_position:
            if self.dragged_chip.state == Chip.board:
                self.snap_chip_to_slot(self.dragged_chip_starting_position)
            elif self.dragged_chip.state == Chip.tray:
                # If the chip was dragged from the tray, snap it back to its original tray position
                self.snap_chip_to_tray_slot(self.dragged_chip_starting_position)
            self.dragged_chip = None
            self.hovering_slot = None
            self.hovering_tray_slot = None
            self.dragged_chip_starting_position = None

            
    def draw(self):
        """
        Draw the board and chips.
        """
        self.window.fill((39,105,127))  # Clear the screen
        self.tray.draw()
        self.draw_lines()
        self.show_hovering_slot()
        self.show_hovering_tray_slot()
        self.draw_draw_chip_button()
        for chip in self.chips:
            if chip.state != Chip.hidden:
                self.window.blit(chip.sprite, (chip.x, chip.y))
                print(chip.state)

    def create_coordinates(self):
        """
        Create visual coordinates for the slots with 5-pixel separation.
        """
        spacing = 1
        for row in range(5):
            for col in range(29):
                x = 3 + col * (BoardInterface.chip_width + spacing)
                y = row * (BoardInterface.chip_height + spacing) * 1.9
                self.board_slots[(row, col)] = (x, y)

    def create_tray_coordinates(self):
        spacing = 5
        for row in range(2):
            for col in range(15):
                x = BoardInterface.chip_width + self.tray.x + col * (BoardInterface.chip_width + spacing)
                y = self.tray.y + row * (BoardInterface.chip_height + spacing)
                self.tray_slots[(row, col)] = (x, y)
       

    def draw_lines(self):
        border_radius = 9  # Adjust for more/less curve
        for (row, col), (x, y) in self.board_slots.items():
            pygame.draw.rect(
                self.window, (255, 255, 255),
                (x, y, BoardInterface.chip_width, BoardInterface.chip_height),
                2, border_radius=border_radius
            )
        for (row, col), (x, y) in self.tray_slots.items():
            pygame.draw.rect(
                self.window, (255, 255, 255),
                (x, y, BoardInterface.chip_width, BoardInterface.chip_height),
                2, border_radius=border_radius
            )

    def draw_draw_chip_button(self):
        """
        Draw a button at the bottom right of the window to draw a chip from the hidden pile.
        """
        button_width, button_height = 180, 60
        margin = 30
        self.button_rect = pygame.Rect(
            self.window.get_width() - button_width - margin,
            self.window.get_height() - button_height - 100,
            button_width,
            button_height
        )
        pygame.draw.rect(self.window, (70, 130, 180), self.button_rect, border_radius=12)
        font = pygame.font.SysFont(None, 36)
        text = font.render("Draw Chip", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.button_rect.center)
        self.window.blit(text, text_rect)

    def handle_draw_chip_button(self, chip_tracker):
        """
        If the draw button is pressed, move a chip from hidden to the tray and add to self.chips.
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if hasattr(self, 'button_rect') and self.button_rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:  # Left mouse button
                self.draw_chip_from_hidden_to_tray(chip_tracker)

    def draw_chip_from_hidden_to_tray(self, chip_tracker):
        """
        Draw a chip from the hidden pile to the tray and add it to self.chips for rendering.
        """
        before = set(chip_tracker.tray_slots.values())
        chip_tracker.place_chip_in_tray_from_hidden()
      
        after = set(chip_tracker.tray_slots.values())
        new_chips = [chip for chip in after if chip and chip not in before]
        for chip in new_chips:
            if chip not in self.chips:
                self.chips.append(chip)
        self.update_chip_coordinates()
        print(self.board_slots[(1, 1)])





