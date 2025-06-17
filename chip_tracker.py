# This module defines a ChipTracker class that manages the placement and removal of chips on a board.
# It provides methods to place, remove, and retrieve chips from specific slots, as well as to get all chips currently on the board.
import random
from chip import Chip
from chip_validator import ChipValidator
from board_grid import BoardGrid
import pygame

class ChipTracker:
    def __init__(self, board_grid, tray_grid):
        self.chips = []
        self.board_grid = board_grid
        self.tray_grid = tray_grid
        self.hidden = []

        # self.board_slots = {}  # Map (row, col) to chips
        # self.board_rows = rows
        # self.board_cols = cols
        # self.tray_slots = {}
        # self.tray_rows = tray_rows  
        # self.tray_cols = tray_cols
        # self.slot_coordinates = {}
        # self.tray_coordinates = {}
        
        # self.hovering_slot = None
        # self.hovering_tray_slot = None
        # self.dragged_chip = None
        # self.dragged_chip_starting_position = None
        


    def drag_chip(self, mouse_x, mouse_y):
        """
        Drag a chip to a new position based on mouse coordinates.
        """
        if self.dragged_chip:
            self.dragged_chip.x = mouse_x - self.dragged_chip.width // 2
            self.dragged_chip.y = mouse_y - self.dragged_chip.height // 2
            self.dragged_chip.update_boundaries()
            

    def place_chip_in_slot(self, chip, row, col): #to add return to origin position
        if self.hovering_slot is not None:
            if self.board_slots[(row, col)] is not None:
                raise ValueError(f"Slot ({row}, {col}) is already occupied!")
            self.board_slots[(row, col)] = chip
            chip.put_chip_in_slot(row, col)
            self.update_chip_coordinates(chip, row, col)
            print(f"Placed chip {chip} in slot ({row}, {col})")
            return
        elif self.hovering_tray_slot is not None:
            if self.tray_slots[(row, col)] is not None:
                raise ValueError(f"Tray slot ({row}, {col}) is already occupied!")
            self.tray_slots[(row, col)] = chip
            chip.put_chip_in_tray(row, col)
            self.update_chip_coordinates(chip, row, col)
            print(f"Placed chip {chip} in tray slot ({row}, {col})")
            return
        print(f"Cannot place chip {chip} in slot ({row}, {col}) - not hovering over a valid slot or tray.")


        
    def place_chip_in_tray_from_hidden(self):
        if not self.hidden:
            print("No hidden chips left!")
            return

        chip = self.hidden.pop()
        for row in range(self.tray_rows):
            for col in range(self.tray_cols):
                if self.tray_slots[(row, col)] is None:
                    self.tray_slots[(row, col)] = chip
                    chip.put_chip_in_tray(row, col)
                    self.update_chip_coordinates(chip, row, col)
                    print(f"Placed chip {chip} in tray slot ({row}, {col}) from hidden")
        print("No available tray slots!")

    def remove_chip(self, chip):
        self.dragged_chip = chip
        self.dragged_chip_starting_position = self.get_chip_position(chip)
        row, col = self.get_chip_position(chip)
        if chip.state == Chip.board:
            self.board_slots[(row, col)] = None
        elif chip.state == Chip.tray:
            self.tray_slots[(row, col)] = None

        raise ValueError(f"Chip {chip} not found in board or tray slots.")
            
    def drag_chip(self, chip, mouse_x, mouse_y):
        """
        Drag a chip to a new position based on mouse coordinates.
        """
        if chip:
            chip.x = mouse_x - chip.width // 2
            chip.y = mouse_y - chip.height // 2
            chip.update_boundaries()
            

    def choose_next_slot(self, snap_range=60):
        """
        Choose the nearest empty slot for the dragged chip within snap_range.
        If the closest slot is occupied, select the next closest empty slot.
        Returns (row, col) if a slot is close enough and empty, else None.
        """
        if not self.dragged_chip:
            self.hovering_slot = None
            return None

        if self.dragged_chip.y < self.window.get_height() - (BoardUI.chip_height / 2) - self.tray.get_height():
            chip_center_x = self.dragged_chip.x + self.dragged_chip.width / 2
            chip_center_y = self.dragged_chip.y + self.dragged_chip.height / 2

            slot_distances = []
            for (row, col), (slot_x, slot_y) in self.board_slots.items():
                slot_center_x = slot_x + BoardUI.chip_width / 2
                slot_center_y = slot_y + BoardUI.chip_height / 2
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


    def create_tray_coordinates(self):
        spacing = 5
        for row in range(2):
            for col in range(15):
                x = ChipTracker.chip_width + self.tray.x + col * (ChipTracker.chip_width + spacing)
                y = self.tray.y + row * (ChipTracker.chip_height + spacing)
                self.tray_slots[(row, col)] = (x, y)

    def get_chip_position(self, chip):
        for (row, col), c in self.board_slots.items():
            if c == chip:
                return (row, col)
        for (row, col), c in self.tray_slots.items():
            if c == chip:
                return (row, col)
        return None
    
    
    def add_testing_chips(self):
        """
        Add testing chips to the board and chip tracker for experimentation.
        """
        for i in range(14):
            self.place_chip_in_tray_from_hidden()


    
# not sure if needed
    def update_chip_coordinates(self, chip, row, col): 
        if self.hovering_slot is not None:
            chip.x , chip.y = self.slot_coordinates[(row, col)]
        elif self.hovering_tray_slot is not None:
            chip.x, chip.y = self.tray_coordinates[(row, col)]

# not sure yet if the 4 methods below are needed
    def get_chip(self, row, col):
        """
        Get the chip in a specific slot.
        """
        return self.board_slots.get((row, col))
    
    def get_chip_from_tray(self, row, col):
        """
        Get the chip in a specific tray slot.
        """
        return self.tray_slots.get((row, col))
    

    def get_all_chips(self):
        """
        Get all chips currently on the board.
        """
        return {slot: chip for slot, chip in self.slots.items() if chip is not None}
    
    def get_all_chips_in_tray(self):
        """
        Get all chips currently in the tray.
        """
        for chip in self.tray_slots.values():
            # print(f'{chip},row: {chip.tray_row}, col: {chip.tray_col}')
            pass

