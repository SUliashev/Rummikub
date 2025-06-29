from src.Config.config import C 
import pygame

class ChipTracker:
    def __init__(self, board_grid, tray_grid, dragging_chip, dispatcher):
        self.dragging_chip = dragging_chip  #can be removed
        self.board_grid = board_grid
        self.tray_grid = tray_grid
        self.dispatcher = dispatcher


        self.hidden_chips = [] 
        


        self.undo_warning_window = False

        self.origin_pos = None
        self.origin_pos_multiple_slots = None
        
        self.hovering_slot = None
        self.multiple_hovering_slots = None # (slot_type, [slots])

        self.selection_start = None  # (x1, y1)
        self.selected_chips = []  #  (slot_type, slots, chips)

        self.dragging_one_chip = False
        self.dragging_multiple_chips = False

        self.move_history = [] 

    def get_chip_at(self, slot_type, slot):
        grid_to_choose_from = self.board_grid.slots if slot_type == 'board' else self.tray_grid.slots
        return grid_to_choose_from[slot]

    def get_position_of_chip(self, search_chip):
        for slot, chip in self.board_grid.slots.items():
            if chip == search_chip:
                return slot
        


      


    def place_chip_in_tray_from_hidden(self):
        if not self.hidden_chips:
            print("No hidden chips left!")
            return

        chip = self.hidden_chips.pop()
        self.tray_grid.put_chip_in_tray_from_hidden(chip)


  



    def undo_all_moves_warning(self):
        if len(self.move_history) > 0:
            self.undo_warning_window = True
        





