from src.Config.config import Config as C

class ChipTracker:
    def __init__(self, board_grid, tray_grid, dragging_chip, dispatcher):
        self.chips_on_board_and_tray = []
        self.dragging_chip = dragging_chip
        self.board_grid = board_grid
        self.tray_grid = tray_grid
        self.origin_pos = None
        self.hidden_chips = [] 
        self.dispatcher = dispatcher
        self.subscribe_events()
        self.search_for_slot = False
        self.hovering_slot = None
        self.mouse_x = 0
        self.mouse_y = 0




    def on_choose_next_slot(self, mouse_x, mouse_y):
        if self.dragging_chip.chip:
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
        chip = self.dragging_chip.chip
        if self.origin_pos[0] == 'tray':
            self.chip_from_dragging_to_tray(self.origin_pos[1])
            
        elif self.origin_pos[0] == 'board':
            self.chip_from_dragging_to_board(self.origin_pos[1])
        self.origin_pos = None
        self.dragging_chip.chip == None


    def chip_from_tray_to_dragging(self, coordinates):
        chip = self.tray_grid.slots.get(coordinates)
        if chip:
            self.tray_grid.slots[coordinates] = None
            self.dragging_chip.chip = chip
            self.origin_pos = ('tray', coordinates)
            return chip
        

    def chip_from_board_to_dragging(self, coordinates):
        chip = self.board_grid.slots.get(coordinates)
        if chip:
            self.board_grid.slots[coordinates] = None
            self.dragging_chip.chip = chip
            self.origin_pos = ('board', coordinates)
            self.hovering_slot = None
            return chip
        

    def chip_from_dragging_to_board(self, coordinates: tuple ):# update later with validation
        chip = self.dragging_chip.chip
        if self.board_grid.slots[coordinates] is None:
            self.dragging_chip.chip = None
            self.origin_pos = None
            self.board_grid.slots[coordinates] = chip
            self.hovering_slot = None
        else:
            self.return_chip_to_origin_pos()


    def chip_from_dragging_to_tray(self, coordinates): #update later with chips moving to the side while hovering
        chip = self.dragging_chip.chip
        if self.tray_grid.slots[coordinates] is None:
            self.dragging_chip.chip = None
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
        self.dispatcher.subscribe('mouse_movement', self.update_mouse_position)
        self.dispatcher.subscribe('mouse_movement', self.on_choose_next_slot)
        self.dispatcher.subscribe('button Draw Chip pressed', self.place_chip_in_tray_from_hidden)
        self.dispatcher.subscribe('button Sort Chips pressed', self.tray_grid.sort_chips_in_tray)

    def update_mouse_position(self, mouse_x, mouse_y, **kwargs):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y



