from src.Config.config import C 
import pygame

class ChipTracker:
    def __init__(self, board_grid, tray_grid, dragging_chip, dispatcher):
        self.dragging_chip = dragging_chip  #can be removed
        self.board_grid = board_grid
        self.tray_grid = tray_grid
        self.dispatcher = dispatcher

        # self.subscribe_events()

        self.hidden_chips = [] 
        
        self.chips_placed_this_turn = []

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



      


    def place_chip_in_tray_from_hidden(self):
        if not self.hidden_chips:
            print("No hidden chips left!")
            return

        chip = self.hidden_chips.pop()
        self.tray_grid.put_chip_in_tray_from_hidden(chip)


    def subscribe_events(self):
        pass
        # self.dispatcher.subscribe('button Draw Chip pressed', self.place_chip_in_tray_from_hidden)
        # self.dispatcher.subscribe('button Undo All Moves pressed', self.undo_all_moves_warning)
        # self.dispatcher.subscribe('start selecting multiple slots', self.select_multiple_slots)
        # self.dispatcher.subscribe('multiple slots selected', self.multiple_slots_selected)
        



    def undo_all_moves_warning(self):
        if len(self.move_history) > 0:
            self.undo_warning_window = True
        
    def undo_all_moves(self):
        for i in range(len(self.move_history)):
            self.undo_last_move()
        self.undo_warning_window = False




