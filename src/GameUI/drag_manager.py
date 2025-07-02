from src.Config.config import C
from src.Core.chip_tracker import ChipTracker
from src.GameUI.dragging_chip import DraggingChip
from src.Core.event_dispatcher import EventDispatcher
from src.Core.chip import Chip
import pygame

class DragManager:
    chip_tracker: ChipTracker
    dragging_chip: DraggingChip
    dispatcher: EventDispatcher
    dragging_one_chip: bool
    dragging_multiple_chips: bool
    origin_pos: tuple[str, tuple[int, int]]
    origin_pos_multiple_slots: tuple[str, list[tuple[int, int]]]
    hovering_slot: tuple[str, tuple[int, int]]
    multiple_hovering_slots: tuple[str, list[tuple[int, int]]]
    selection_start: tuple[int, int]
    selected_chips: list[Chip]

    def __init__(self, chip_tracker: ChipTracker, dragging_chip: DraggingChip, dispatcher: EventDispatcher):
        self.chip_tracker = chip_tracker
        self.dragging_chip = dragging_chip
        self.dispatcher = dispatcher
        self.dragging_one_chip = False
        self.dragging_multiple_chips = False
        self.origin_pos = None
        self.origin_pos_multiple_slots = None
        self.hovering_slot = None
        self.multiple_hovering_slots = None
        self.selection_start = None
        self.selected_chips = None


    def get_grid(self, grid_type: str) -> dict[tuple[int, int], Chip]:
        return self.chip_tracker.board_grid.slots if grid_type == 'board' else self.chip_tracker.tray_grid.slots


    def start_dragging_chip(self, grid_type: str, slot: tuple[int, int], chip: Chip) -> None:
        self.dragging_one_chip = True
        self.dragging_chip.set_one_chip(chip)
        self.origin_pos = (grid_type, slot)
        self.dispatcher.dispatch('chip_picked_up', grid_type=grid_type, slot=slot )


    def choose_next_single_slot(self, mouse_x: int, mouse_y:int):
        snap_range = 60

        def find_nearest_empty_slot(slot_coordinates: tuple[int, int] , slots_dict:dict[tuple[int, int], tuple[int, int]] ):
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


    def chip_from_dragging_to_grid(self) -> None:
        chip = self.dragging_chip.main_chip
        self.dispatcher.dispatch('chip placed on slot', hovering_slot=self.hovering_slot, chip=chip, origin_pos=self.origin_pos )
        self.dragging_chip.clear()
        self.dragging_one_chip = False   
        self.origin_pos = None
        self.hovering_slot = None


    def select_multiple_slots(self, mouse_x: int, mouse_y: int) -> None:
        if not self.dragging_chip.chips:
            self.selection_start = (mouse_x, mouse_y)


    def multiple_slots_selected(self, ending_x_y: tuple[int, int]) -> None:
        if self.selection_start:
            self.select_chips_in_rectangle(self.selection_start, ending_x_y)
            self.selection_start = None


    def select_chips_in_rectangle(self, selection_start: tuple[int, int], selection_end: tuple[int, int]) -> None:    # I think None chips are added now, might not work at first yet
        x1, y1 = selection_start
        x2, y2 = selection_end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1))
        
        self.selection_start = None

        candidate_rows = []

        visible_tray_rows_start, visible_tray_rows_end = self.chip_tracker.tray_grid.visible_row_start, self.chip_tracker.tray_grid.visible_row_start + 2
        range_of_rows = range(visible_tray_rows_start, visible_tray_rows_end)
        rows = (range(C.board_rows), range_of_rows)
        cols = (C.board_cols, C.tray_cols)
        grid = (self.chip_tracker.board_grid.slots, self.chip_tracker.tray_grid.slots)
        slot_coord = (C.board_slot_coordinates, C.tray_slot_coordinates)
        grid_type = ('board', 'tray')
        # Check all rows
        for i in range(2):
            for row in rows[i]:
                chips_in_row = []
                chip_positions = []
                for col in range(cols[i]):
                    chip = grid[i].get((row, col))
                    chip_x, chip_y = slot_coord[i][(row, col)]
                    chip_rect = pygame.Rect(chip_x, chip_y, C.chip_width, C.chip_height)
                    if rect.colliderect(chip_rect):
                        chips_in_row.append(chip)
                        chip_positions.append((row, col))
                # Only add row if it contains at least one non-None chip
                if any(chip is not None for chip in chips_in_row):
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


    def start_dragging_selected_chips(self, chip: Chip) -> None:
        self.selection_start = None

        if chip not in self.selected_chips[2]:
            self.selected_chips = None
            return
        
        grid_type, chip_positions, chips = self.selected_chips

       
        selected_chip_index = next((indx for indx, item in enumerate(chips) if chip == item))
        leftmost_chip_index = min(indx for indx, item in enumerate(chips) if item is not None)
        rightmost_chip_index = max(indx for indx, item in enumerate(chips) if item is not None)
       

        left_chips = []
        for indx in range(leftmost_chip_index, selected_chip_index):
            left_chips.append(chips[indx])
        
        main_chip = chips[selected_chip_index]

        right_chips = []
        for indx in range(selected_chip_index + 1, rightmost_chip_index +1):
            right_chips.append(chips[indx])
        
        chip_positions = chip_positions[leftmost_chip_index:rightmost_chip_index +1]

        self.dispatcher.dispatch('multiple chips picked up',grid_type=grid_type, chip_positions=chip_positions )
    
        chips = left_chips + [main_chip] + right_chips

        self.dragging_chip.chips = chips  # All in-range chips (including None)
        self.dragging_chip.main_chip = main_chip
        self.dragging_chip.chips_to_left = left_chips
        self.dragging_chip.chips_to_right = right_chips
        self.origin_pos_multiple_slots = (grid_type, chip_positions)
        self.selected_chips = None
        self.dragging_multiple_chips = True 


    def choose_multiple_hovering_slots(self) -> None:
        if not self.hovering_slot or self.hovering_slot[1] is None:
            return
        
        grid_type, (hovering_row, hovering_col) = self.hovering_slot  
      
        grid = self.get_grid(grid_type)
        max_type = C.tray_cols if grid_type == 'tray' else C.board_cols

        slots_to_draw = []
        chips_to_choose_from = self.dragging_chip.chips

        if self.dragging_chip.chips_to_left:
            left_most_col = hovering_col - len(self.dragging_chip.chips_to_left)
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


    def place_dragging_chips(self) -> None:
        chips = self.dragging_chip.chips
        self.dispatcher.dispatch('multiple chips placed', hovering_slots=self.multiple_hovering_slots,  chips=chips, origin_pos=self.origin_pos_multiple_slots )
        self.dragging_chip.clear()
        self.dragging_multiple_chips = False
        self.origin_pos_multiple_slots = None
        self.hovering_slot = None


    def choose_next_slots(self, mouse_x: int, mouse_y: int) -> None:
        if self.dragging_one_chip:
            self.choose_next_single_slot(mouse_x, mouse_y)
        elif self.dragging_multiple_chips:
            self.choose_next_single_slot(mouse_x, mouse_y)
            self.choose_multiple_hovering_slots()


    def mouse_button_down_actions(self, mouse_x: int, mouse_y: int) -> bool:
        if self.is_mouse_over_slot(mouse_x, mouse_y):
            slot_type, slot = self.is_mouse_over_slot(mouse_x, mouse_y)
            chip = self.chip_tracker.get_chip_at(slot_type, slot)
            if chip:
                if self.selected_chips:
                    self.start_dragging_selected_chips(chip)
                else:
                    self.start_dragging_chip(slot_type, slot, chip)
                return True
            else:
                self.select_multiple_slots(mouse_x, mouse_y)
        else:
            self.select_multiple_slots(mouse_x, mouse_y)


    def mouse_button_up_actions(self, mouse_x: int, mouse_y: int) -> None:
        if self.dragging_one_chip: 
            self.chip_from_dragging_to_grid()
            return
        
        elif self.dragging_multiple_chips: # to add event dispatcher for validation
            self.place_dragging_chips()
            return
  
        if self.selection_start:
            self.multiple_slots_selected((mouse_x, mouse_y))


    def is_mouse_over_slot(self, mouse_x: int, mouse_y: int) -> tuple[int, int]:
        if self.is_mouse_over_board(mouse_x, mouse_y):
            for (row, col), (x, y) in C.board_slot_coordinates.items():
                slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    return ('board', (row, col))
        if self.is_mouse_over_tray(mouse_x, mouse_y):
            for (row, col), (x, y) in C.tray_slot_coordinates.items():
                slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    return ( 'tray', (row, col))
        return False


    def is_mouse_over_board(self, mouse_x: int, mouse_y: int) -> bool:
        y_correct = mouse_y < C.tray_background_y
        return y_correct
       

    def is_mouse_over_tray(self, mouse_x: int, mouse_y: int) -> bool:
        tray_rect = pygame.Rect(C.tray_background_x, C.tray_background_y, C.tray_background_width, C.tray_background_height)
        return tray_rect.collidepoint(mouse_x, mouse_y)


            


