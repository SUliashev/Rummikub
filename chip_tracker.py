# This module defines a ChipTracker class that manages the placement and removal of chips on a board.
# It provides methods to place, remove, and retrieve chips from specific slots, as well as to get all chips currently on the board.
import random
from chip import Chip
from chip_validator import ChipValidator
from board_grid import BoardGrid
import pygame

class ChipTracker:
    def __init__(self, board_grid, tray_grid, dragging_chip):
        
        self.chips_on_board_and_tray = []
        self.dragging_chip = dragging_chip
        self.board_grid = board_grid
        self.tray_grid = tray_grid
        self.origin_pos = None
        self.hidden_chips = []
        
        # self.hovering_slot = None
        # self.hovering_tray_slot = None
        # self.dragged_chip = None
        # self.dragged_chip_starting_position = None
        
    def return_chip_to_origin_pos(self):
        chip = self.dragging_chip.chip
        if self.origin_pos[0] == 'tray':
            self.tray_grid.slots[self.origin_pos[1]] = chip
        elif self.origin_pos[0] == 'board':
            self.board_grid.slots[self.origin_pos[1]] = chip
        self.dragging_chip.chip == None


    def chip_from_tray_to_dragging(self, row, col):
        """
        Move a chip from the tray to the dragging state.
        """
        chip = self.tray_grid.slots.get((row, col))
        if chip:
            self.tray_grid.slots[(row, col)] = None
            self.dragging_chip.chip = chip
            self.origin_pos = ('tray', (row, col))
            return chip
    
    def chip_from_dragging_to_board(self, coordinates: tuple ):# update later with validation
        chip = self.chip_tracker.dragging_chip.chip
        if self.board_grid.slot(coordinates) is None:
            self.dragging_chip.chip = None
            self.board_grid.slot[coordinates] = chip
        else:
            self.return_chip_to_origin_pos()

    def chip_from_draggin_to_tray(self, coordinates): #update later with chips moving to the side while hovering
        chip = self.chip_tracker.dragging_chip.chip
        if self.tray_grid.slot(coordinates) is None:
            self.dragging_chip.chip = None
            self.tray_grid.slot[coordinates] = chip
        else:
            self.return_chip_to_origin_pos()


    def place_chip_in_tray_from_hidden(self):
        if not self.hidden_chips:
            print("No hidden chips left!")
            return

        chip = self.hidden_chips.pop()
        self.tray_grid.put_chip_in_tray_from_hidden(chip)

        
    # def chip_from_draggin_to_slot(self):
    #     if self.chip_tracker.moving_chip:
    #         if 


    def add_testing_chips(self):
        """
        Add testing chips to the board and chip tracker for experimentation.
        """
        for i in range(14):
            self.place_chip_in_tray_from_hidden()


        # def choose_next_slot(self, snap_range=60):
    #     """
    #     Choose the nearest empty slot for the dragged chip within snap_range.
    #     If the closest slot is occupied, select the next closest empty slot.
    #     Returns (row, col) if a slot is close enough and empty, else None.
    #     """
    #     if not self.dragged_chip:
    #         self.hovering_slot = None
    #         return None

    #     if self.dragged_chip.y < self.window.get_height() - (BoardUI.chip_height / 2) - self.tray.get_height():
    #         chip_center_x = self.dragged_chip.x + self.dragged_chip.width / 2
    #         chip_center_y = self.dragged_chip.y + self.dragged_chip.height / 2

    #         slot_distances = []
    #         for (row, col), (slot_x, slot_y) in self.board_slots.items():
    #             slot_center_x = slot_x + BoardUI.chip_width / 2
    #             slot_center_y = slot_y + BoardUI.chip_height / 2
    #             distance = ((chip_center_x - slot_center_x) ** 2 + (chip_center_y - slot_center_y) ** 2) ** 0.5
    #             if distance <= snap_range:
    #                 slot_distances.append((distance, (row, col)))

    #         slot_distances.sort(key=lambda x: x[0])
    #         for _, (row, col) in slot_distances:
    #             if self.chip_tracker.get_chip(row, col) is None:
    #                 self.hovering_slot = (row, col)
    #                 self.hovering_tray_slot = None
    #                 return (row, col)

    # If no slot is in range, clear hovering
        # self.hovering_slot = None
        # return None




