# This module defines a ChipTracker class that manages the placement and removal of chips on a board.
# It provides methods to place, remove, and retrieve chips from specific slots, as well as to get all chips currently on the board.
import random
from chip import Chip
from chip_validator import ChipValidator
class ChipTracker:
    def __init__(self, rows=5, cols=29, tray_rows=2, tray_cols=15):
        self.slots = {}  # Map (row, col) to chips
        self.rows = rows
        self.cols = cols
        self.tray_slots = {}
        self.tray_rows = tray_rows  
        self.tray_cols = tray_cols
        self.hidden = []
        
        # Initialize empty slots
        for row in range(rows):
            for col in range(cols):
                self.slots[(row, col)] = None  # None means the slot is empty
    
        for tray_row in range(tray_rows):
            for tray_col in range(tray_cols):
                self.tray_slots[(tray_row, tray_col)] = None

    def place_chip(self, chip, row, col):
        """
        Place a chip in a specific slot.
        """
        if self.slots[(row, col)] is not None:
            raise ValueError(f"Slot ({row}, {col}) is already occupied!")
        self.slots[(row, col)] = chip
        chip.put_chip_in_slot(row, col)
        # print(f"Placed chip {chip} at ({row}, {col})")

    def place_chip_in_tray(self, chip, row, col):
        """
        Place a chip in a specific tray slot.
        """
        if self.tray_slots.get((row, col)) is not None and self.tray_slots[(row, col)] != chip:
            self.place_chip_in_first_tray_slot(chip)
            return
        self.tray_slots[(row, col)] = chip
        chip.put_chip_in_tray(row, col)
        # print(f"Placed chip {chip} in tray at ({row}, {col})")

        
    def place_chip_in_tray_from_hidden(self):
        """
        Take a chip from the hidden pile and place it in the first available tray slot.
        """
        if not self.hidden:
            print("No hidden chips left!")
            return

        chip = self.hidden.pop()
        for row in range(self.tray_rows):
            for col in range(self.tray_cols):
                if self.tray_slots.get((row, col)) is None:
                    self.tray_slots[(row, col)] = chip
                    chip.put_chip_in_tray(row, col)
                    print(f"Placed chip {chip} in tray at ({row}, {col})")
                    return
        print("No available tray slots!")

    def remove_chip(self, chip, row: int, col: int):
        """
        Remove a chip from a specific slot.
        """
        chip.remove_chip_from_slot()
        self.slots[(row, col)] = None
   

    def get_chip(self, row, col):
        """
        Get the chip in a specific slot.
        """
        return self.slots.get((row, col))
    
    def get_chip_from_tray(self, row, col):
        """
        Get the chip in a specific tray slot.
        """
        return self.tray_slots.get((row, col))
    
    def remove_chip_from_tray(self, chip, row: int, col: int):
        """
        Remove a chip from a specific tray slot.
        """
        self.tray_slots[(row, col)] = None
        chip.remove_chip_from_tray()
        # print(f"Removed chip {chip} from tray at ({row}, {col})")

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

