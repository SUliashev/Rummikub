# This module defines a ChipTracker class that manages the placement and removal of chips on a board.
# It provides methods to place, remove, and retrieve chips from specific slots, as well as to get all chips currently on the board.
class ChipTracker:
    def __init__(self, rows=5, cols=29):
        self.slots = {}  # Map (row, col) to chips
        self.validation_slots = {}  # Map (row, col) to validation status
        self.rows = rows
        self.cols = cols

        # Initialize empty slots
        for row in range(rows):
            for col in range(cols):
                self.slots[(row, col)] = None  # None means the slot is empty
                self.validation_slots[(row, col)] = None  # Initially, all slots are valid

    def validate_chip(self, chip, row, col):
        if self.slots[(row, col)] is not None:
            raise ValueError(f"Slot ({row}, {col}) is already occupied! (validation)")
        self.validation_slots[(row, col)] = chip  # Mark the slot as valid
        

    def place_chip(self, chip, row, col):
        """
        Place a chip in a specific slot.
        """
        if self.slots[(row, col)] is not None:
            raise ValueError(f"Slot ({row}, {col}) is already occupied!")
        self.slots[(row, col)] = chip
        self.validation_slots[(row, col)] = chip  # Mark the slot as valid
        chip.put_chip_in_slot(row, col)
        print(f"Placed chip {chip} at ({row}, {col})")
        

    def remove_chip(self, chip, row: int, col: int):
        """
        Remove a chip from a specific slot.
        """
        chip.remove_chip_from_slot()
        self.slots[(row, col)] = None
        self.validation_slots[(row, col)] = None
       

    def get_chip(self, row, col):
        """
        Get the chip in a specific slot.
        """
        return self.slots.get((row, col))
    
    def get_validation_chip(self, row, col):
        return self.validation_slots.get((row, col))

    def get_all_chips(self):
        """
        Get all chips currently on the board.
        """
        return {slot: chip for slot, chip in self.slots.items() if chip is not None}