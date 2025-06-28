from src.Config.config import C
import pygame

class DragManager:
    def __init__(self, chip_tracker, dragging_chip, move_manager):
        self.chip_tracker = chip_tracker
        self.dragging_chip = dragging_chip
        self.move_manager = move_manager
        self.dragging_one_chip = False
        self.dragging_multiple_chips = False
        self.origin_pos = None
        self.origin_pos_multiple_slots = None
        self.hovering_slot = None
        self.multiple_hovering_slots = None
        self.selection_start = None
        self.selected_chips = None

    def get_grid(self, grid_type: str):
        return self.chip_tracker.board_grid.slots if grid_type == 'board' else self.chip_tracker.tray_grid.slots


    def place_dragging_chips(self):
        chips = self.dragging_chip.chips

        if not self.multiple_hovering_slots:
            valid_move = False
        if not self.chip_validator.validate_move():
            valid_move = False
        if self.multiple_hovering_slots[0] == 'tray':
            for chip in chips:
                if chip not in self.move_manager.chips_placed_this_turn:
                    valid_move =False
                    self.dispatcher.dispatch('cannot take chips from the board')
                    break

        if valid_move:
            grid_type, target_slots = self.multiple_hovering_slots
        else:
            grid_type, target_slots = self.origin_pos_multiple_slots
    
        grid_slots = self.get_grid(grid_type)

        # for slot in target_slots:
        #     if grid_slots[slot] is not None:
        #         self.place_dragging_chips(*self.origin_pos_multiple_slots)
        #         return
            
        
        if valid_move:
            self.move_manager.move_history.append({
                'action': 'place_multiple_chips',
                'chip': chips,
                'from': self.origin_pos_multiple_slots,
                'to': (grid_type, target_slots)
            })

        for indx, chip in enumerate(chip for chip in chips if chip is not None):
            grid_slots[target_slots[indx]] = chip


        if grid_type == 'board':
            for chip in chips:
                if chip not in self.move_managerchips_placed_this_turn:
                    self.move_manager.chips_placed_this_turn.append(chip)
        elif grid_type == 'tray':
            for chip in chips:
                if chip in self.chips_placed_this_turn:
                    self.move_manager.chips_placed_this_turn.remove(chip)
        
        self.dragging_chip.clear()
        self.dragging_multiple_chips = False
        self.origin_pos_multiple_slots = None
        self.hovering_slot = None
        self.chip_validator.validate_current_state()
        return True
    
    
    

    def chip_from_dragging_to_grid(self, returned=False ):
        chip = self.dragging_chip.main_chip

        self.move_manager.move_single_chip_to(self.hovering_slot, chip, self.origin_pos)

        self.dragging_chip.clear()
        self.dragging_one_chip = False   #perhaps can be removed
        self.origin_pos = None
        self.hovering_slot = None



    def start_dragging_chip(self, grid_type, slot, chip):
        self.dragging_one_chip = True
        self.dragging_chip.set_one_chip(chip)
        self.origin_pos = (grid_type, slot)
        self.move_manager.chip_picked_up(grid_type, slot)
    
                 

    def start_dragging_selected_chips(self, chip):
        self.selection_start = None

        grid_type, chip_positions, chips = self.selected_chips

        if chip not in chips:
            self.selected_chips = None
            return
        
        grid = self.get_grid(grid_type)
        
        selected_chip_index = next((indx for indx, item in enumerate(chips) if chip == item))
        leftmost_chip_index = min(indx for indx, item in enumerate(chips) if item is not None)
        rightmost_chip_index = max(indx for indx, item in enumerate(chips) if item is not None)
       

        left_chips = []
        for indx in range(leftmost_chip_index, selected_chip_index):
            left_chips.append(chips[indx])
        
        main_chip = chips[selected_chip_index]

        right_chips = []
        for indx in range(selected_chip_index + 1, rightmost_chip_index):
            right_chips.append(chips[indx])
        
        chip_positions = chip_positions[leftmost_chip_index:rightmost_chip_index]
    
        for slot in chip_positions:
            grid[slot] = None

        chips = left_chips + [main_chip] + right_chips

        self.dragging_chip.chips = chips  # All in-range chips (including None)
        self.dragging_chip.main_chip = main_chip
        self.dragging_chip.left_chips = left_chips
        self.dragging_chip.right_chips = right_chips
        self.dragging_chip.chip_positions = chip_positions
        self.dragging_chip.main_chip_index = selected_chip_index
        self.origin_pos_multiple_slots = (grid_type, chip_positions)
        self.selected_chips = None
        self.dragging_multiple_chips = True
        self.chip_validator.validate_current_state()

    def select_chips_in_rectangle(self, selection_start, selection_end):    # I think None chips are added now, might not work at first yet
        x1, y1 = selection_start
        x2, y2 = selection_end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1))
        
        self.selection_start = None

        candidate_rows = []

        rows = (C.board_rows, C.tray_rows)
        cols = (C.board_cols, C.tray_cols)
        grid = (self.chip_tracker.board_grid.slots, self.chip_tracker.tray_grid.slots)
        slot_coord = (C.board_slot_coordinates, C.tray_slot_coordinates)
        grid_type = ('board', 'tray')
        # Check all rows
        for i in range(2):
            for row in range(rows[i]):
                chips_in_row = []
                chip_positions = []
                for col in range(cols[i]):
                    chip = grid[i].get((row, col))
                    chip_x, chip_y = slot_coord[i][(row, col)]
                    chip_rect = pygame.Rect(chip_x, chip_y, C.chip_width, C.chip_height)
                    if rect.colliderect(chip_rect):
                        chips_in_row.append(chip)
                        chip_positions.append((row, col))

                if chips_in_row:
                    _, row_y = slot_coord[i][(row, 0)]
                    row_center_y = row_y + C.chip_height // 2
                    candidate_rows.append((grid_type[i], row, row_center_y, chip_positions, chips_in_row))

        if not candidate_rows:
            self.selected_chips = None
            return

        # Sort candidate rows by distance to selection_start y
        candidate_rows.sort(key=lambda tup: abs(y1 - tup[2]))

        # Try each candidate row in order of proximity
        selected_type = None
        for row_type, row, row_center_y, chip_positions, chips_in_row in candidate_rows:
            if chips_in_row:
                if selected_type is None:
                    selected_type = row_type
                elif selected_type != row_type:
                    self.selected_chips = None
                    return
                self.selected_chips = (row_type, chip_positions, chips_in_row)
                return

        # If no chips found in any row
        self.selected_chips = None     


    def multiple_slots_selected(self, ending_x_y):
        if self.selection_start:
            self.select_chips_in_rectangle(self.selection_start, ending_x_y)
            self.selection_start = None


    def select_multiple_slots(self, mouse_x, mouse_y):
        if not self.dragging_chip.chips:
            self.selection_start = (mouse_x, mouse_y)


    def choose_multiple_hovering_slots(self):
        if not self.hovering_slot:
            return
        
        grid_type, (hovering_row, hovering_col) = self.hovering_slot  
      
        grid = self.get_grid(grid_type)
        max_type = C.tray_cols if grid_type == 'tray' else C.board_cols

        slots_to_draw = []
        chips_to_choose_from = self.dragging_chip.chips

        if self.dragging_chip.left_chips:
            left_most_col = hovering_col - len(self.dragging_chip.left_chips)
        else:
            left_most_col = hovering_col

        for idx, chip in enumerate(chips_to_choose_from):
            if chip is not None:
                slots_to_draw.append((hovering_row, (idx + left_most_col)))

        cols = [slot[1] for slot in slots_to_draw]
        if min(cols) < 0 or max(cols) > max_type -1:
            self.multiple_hovering_slots = None
            return

        for row, col in slots_to_draw:
            if grid[row, col] is not None:
                self.multiple_hovering_slots = None
                return
        
        self.multiple_hovering_slots = (grid_type, slots_to_draw)


    def choose_next_single_slot(self, mouse_x, mouse_y):
        snap_range = 60


        def find_nearest_empty_slot(slot_coordinates, slots_dict):
            slot_distances = []
            for (row, col), (slot_x, slot_y) in slot_coordinates.items():
                slot_center_x = slot_x + C.chip_width // 2
                slot_center_y = slot_y + C.chip_height // 2
                distance = int(((mouse_x - slot_center_x) ** 2 + (mouse_y - slot_center_y) ** 2) ** 0.5)
                if distance <= snap_range and slots_dict[(row, col)] is None:
                    slot_distances.append((distance, (row, col)))
            if slot_distances:
                slot_distances.sort(key=lambda x: x[0])
                return slot_distances[0][1]
            return None


        slots_to_check = None
        if mouse_y <= C.tray_background_y:
            slots_to_check = self.chip_tracker.board_grid.slots 
            coordinates = C.board_slot_coordinates
            grid_type = 'board'
        elif pygame.Rect(C.tray_background).collidepoint(mouse_x, mouse_y):
            slots_to_check = self.chip_tracker.tray_grid.slots 
            grid_type = 'tray'
            coordinates = C.tray_slot_coordinates

        if not slots_to_check:
            self.hovering_slot = None
            return
        
        next_slot = find_nearest_empty_slot(
            coordinates,
            slots_to_check)

        self.hovering_slot = (grid_type, next_slot)


    def choose_next_slots(self, mouse_x, mouse_y):
        if self.dragging_one_chip:
            self.choose_next_single_slot(mouse_x, mouse_y)
        elif self.dragging_multiple_chips:
            self.choose_next_single_slot(mouse_x, mouse_y)
            self.choose_multiple_hovering_slots()
            


