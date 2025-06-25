from src.Config.config import C 
import pygame

class ChipTracker:
    def __init__(self, board_grid, tray_grid, dragging_chip, dispatcher):
        self.dragging_chip = dragging_chip
        self.board_grid = board_grid
        self.tray_grid = tray_grid
        self.dispatcher = dispatcher
        self.subscribe_events()

        self.hidden_chips = [] 

        self.origin_pos = None
        self.origin_pos_multiple_slots = None
        
        self.hovering_slot = None
        self.multiple_hovering_slots = None # (slot_type, [slots])

        self.selection_start = None  # (x1, y1)
        self.selected_chips = []  #  (slot_type, slots, chips)

        self.dragging_one_chip = False
        self.dragging_multiple_chips = False



    def place_multiple_chips_in_slots(self):
        if self.multiple_hovering_slots:
            grid_type, target_slots = self.multiple_hovering_slots
            self.place_dragging_chips(grid_type, target_slots)
        else:
            self.place_dragging_chips(*self.origin_pos_multiple_slots)

    def place_dragging_chips(self, grid_type, target_slots):

        if grid_type == 'board':
            grid_slots = self.board_grid.slots
        else:
            grid_slots = self.tray_grid.slots

        for slot in target_slots:
            if grid_slots[slot] is not None:
                self.place_dragging_chips(*self.origin_pos_multiple_slots)
                return
            
        chips = self.dragging_chip.left_chips + [self.dragging_chip.main_chip] + self.dragging_chip.right_chips
        print(chips)
        print(target_slots)
        for indx, chip in enumerate(chip for chip in chips if chip is not None):
            grid_slots[target_slots[indx]] = chip


        self.dragging_chip.clear()
        self.dragging_multiple_chips = False
        self.origin_pos_multiple_slots = None
        self.hovering_slot = None
        return True
    
    def start_dragging_selected_chips(self, mouse_x, mouse_y):
        row_type, chip_positions, chips = self.selected_chips
      
        self.selection_start = None  # (x1, y1)


        # print(chip_positions)

        leftmost_col = chip_positions[0][1]
        rightmost_col = chip_positions[-1][1]

        # Find which chip was clicked
        clicked_row = None
        if row_type == 'tray':
            slots_to_check = C.tray_slot_coordinates
            grid_to_check = self.tray_grid.slots
        else:
            slots_to_check = C.board_slot_coordinates
            grid_to_check = self.board_grid.slots

        for ind, (row, col) in enumerate(chip_positions):
            chip_x, chip_y = slots_to_check[(row, col)]
            chip_rect = pygame.Rect(chip_x, chip_y, C.chip_width, C.chip_height)
            if chip_rect.collidepoint(mouse_x, mouse_y):
                clicked_row = row
                clicked_col = col
                clicked_index = abs(leftmost_col - clicked_col)
                # clicked_chip = grid_to_check[(row, col)]
                break

        if clicked_row is None:
            self.selected_chips = []
            return False  # No chip was clicked

        left_chips = []
        for col in range(leftmost_col,clicked_col):
            left_chips.append(grid_to_check[(clicked_row, col)])
        
        main_chip = grid_to_check[(clicked_row, clicked_col)]

        right_chips = []
        for col in range(clicked_col + 1, rightmost_col + 1):
            right_chips.append(grid_to_check[(clicked_row, col)])
        
        # chips = left_chips + main_chip + right_chips

        for slot in chip_positions:
            grid_to_check[slot] = None

        chips = left_chips + [main_chip] + right_chips

        self.dragging_chip.chips = chips  # All in-range chips (including None)
        self.dragging_chip.main_chip = main_chip
        self.dragging_chip.left_chips = left_chips
        self.dragging_chip.right_chips = right_chips
        self.dragging_chip.chip_positions = chip_positions
        self.dragging_chip.main_chip_index = clicked_index
        self.origin_pos_multiple_slots = (row_type, chip_positions)
        print(row_type)
        self.selected_chips = None

        self.dragging_multiple_chips = True


    
    def select_chips_in_rectangle(self, selection_start, selection_end):
        x1, y1 = selection_start
        x2, y2 = selection_end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1))
        
        self.selection_start = None

        candidate_rows = []

        # Check board rows
        for row in range(C.board_rows):
            chips_in_row = []
            chip_positions = []
            for col in range(C.board_cols):
                chip = self.board_grid.slots.get((row, col))
                if chip:
                    chip_x, chip_y = C.board_slot_coordinates[(row, col)]
                    chip_rect = pygame.Rect(chip_x, chip_y, C.chip_width, C.chip_height)
                    if rect.colliderect(chip_rect):
                        chips_in_row.append(chip)
                        chip_positions.append((row, col))
            if chips_in_row:
                _, row_y = C.board_slot_coordinates[(row, 0)]
                row_center_y = row_y + C.chip_height // 2
                candidate_rows.append(('board', row, row_center_y, chip_positions, chips_in_row))

        # Check tray rows
        for row in range(C.tray_rows):
            chips_in_row = []
            chip_positions = []
            for col in range(C.tray_cols):
                chip = self.tray_grid.slots.get((row, col))
                if chip:
                    chip_x, chip_y = C.tray_slot_coordinates[(row, col)]
                    chip_rect = pygame.Rect(chip_x, chip_y, C.chip_width, C.chip_height)
                    if rect.colliderect(chip_rect):
                        chips_in_row.append(chip)
                        chip_positions.append((row, col))
            if chips_in_row:
                _, row_y = C.tray_slot_coordinates[(row, 0)]
                row_center_y = row_y + C.chip_height // 2
                candidate_rows.append(('tray', row, row_center_y, chip_positions, chips_in_row))

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
        
        slot_type, (hovering_row, hovering_col) = self.hovering_slot  
      
        if slot_type == 'tray':
            grid = self.tray_grid.slots
            # slot_coordinates = C.tray_slot_coordinates
            max_type = C.tray_cols
        elif slot_type == 'board':
            grid = self.board_grid.slots
            # slot_coordinates = C.board_slot_coordinates
            max_type = C.board_cols

        slots_to_draw = []
        chips_to_choose_from = self.dragging_chip.left_chips + [self.dragging_chip.main_chip] + self.dragging_chip.right_chips

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
        
        self.multiple_hovering_slots = (slot_type, slots_to_draw)

    def on_choose_next_slot(self, mouse_x, mouse_y):
        if self.dragging_chip.chips:
            snap_range = 60
            chip_center_x = mouse_x 
            chip_center_y = mouse_y 

            def find_nearest_empty_slot(slot_coordinates, slots_dict):
                slot_distances = []
                for (row, col), (slot_x, slot_y) in slot_coordinates.items():
                    slot_center_x = slot_x + C.chip_width // 2
                    slot_center_y = slot_y + C.chip_height // 2
                    distance = int(((chip_center_x - slot_center_x) ** 2 + (chip_center_y - slot_center_y) ** 2) ** 0.5)
                    if distance <= snap_range and slots_dict[(row, col)] is None:
                        slot_distances.append((distance, (row, col)))
                if slot_distances:
                    slot_distances.sort(key=lambda x: x[0])
                    return slot_distances[0][1]
                return None

            if mouse_y <= C.tray_background_y:
                next_slot = find_nearest_empty_slot(
                    C.board_slot_coordinates,
                    self.board_grid.slots
                )
                if next_slot:
                    self.hovering_slot = ('board', next_slot)
                    return

            elif C.tray_background_x < mouse_x < C.tray_background_x + C.tray_background_width and mouse_y > C.tray_background_y:
                next_slot = find_nearest_empty_slot(
                    C.tray_slot_coordinates,
                    self.tray_grid.slots
                )
                if next_slot:
                    self.hovering_slot = ('tray', next_slot)
                    return

            self.hovering_slot = None
            


    def return_chip_to_origin_pos(self):
        chip = self.dragging_chip.main_chip
        if self.origin_pos[0] == 'tray':
            self.chip_from_dragging_to_tray(self.origin_pos[1])
            
        elif self.origin_pos[0] == 'board':
            self.chip_from_dragging_to_board(self.origin_pos[1])
        self.origin_pos = None
        self.dragging_chip.clear()


    def chip_from_tray_to_dragging(self, coordinates):
        chip = self.tray_grid.slots.get(coordinates)
        if chip:
            self.tray_grid.slots[coordinates] = None
            self.dragging_one_chip = True
            self.dragging_chip.chips = [chip]
            self.dragging_chip.main_chip = chip
            self.origin_pos = ('tray', coordinates)
            return True
        

    def chip_from_board_to_dragging(self, coordinates):
        chip = self.board_grid.slots.get(coordinates)
        if chip:
            self.board_grid.slots[coordinates] = None
            self.dragging_chip.chips = [chip]
            self.dragging_chip.main_chip = chip
            self.dragging_one_chip = True
            self.origin_pos = ('board', coordinates)
            return chip
        

    def chip_from_dragging_to_board(self, coordinates: tuple ):# update later with validation
        chip = self.dragging_chip.main_chip
        if self.board_grid.slots[coordinates] is None:
            self.dragging_chip.clear()
            self.dragging_one_chip = False
            self.origin_pos = None
            self.board_grid.slots[coordinates] = chip
            self.hovering_slot = None
        else:
            self.return_chip_to_origin_pos()


    def chip_from_dragging_to_tray(self, coordinates): #update later with chips moving to the side while hovering
        chip = self.dragging_chip.main_chip
        if self.tray_grid.slots[coordinates] is None:
            self.dragging_chip.clear()
            self.dragging_one_chip = False
            self.origin_pos = None
            self.tray_grid.slots[coordinates] = chip
            self.hovering_slot = None
        else:
            self.return_chip_to_origin_pos()


    def place_chip_in_tray_from_hidden(self):
        if not self.hidden_chips:
            print("No hidden chips left!")
            return

        chip = self.hidden_chips.pop()
        self.tray_grid.put_chip_in_tray_from_hidden(chip)


    def subscribe_events(self):
       
        self.dispatcher.subscribe('button Draw Chip pressed', self.place_chip_in_tray_from_hidden)
        self.dispatcher.subscribe('button Sort Chips pressed', self.tray_grid.sort_chips_in_tray)
        self.dispatcher.subscribe('start selecting multiple slots', self.select_multiple_slots)
        self.dispatcher.subscribe('multiple slots selected', self.multiple_slots_selected)






