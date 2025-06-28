class MoveManager:
    def __init__(self, chip_tracker, chip_validator, dispatcher):
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator
        self.dispatcher = dispatcher
        self.move_history = []
        self.chips_placed_this_turn = []

    def get_grid(self, grid_type):
        return self.chip_tracker.board_grid.slots if grid_type == 'board' else self.chip_tracker.tray_grid.slots
    
    def move_single_chip_to(self, hovering_slot, chip, origin_pos):
        to_type, to_slot = hovering_slot

        valid_move = True
        if not hovering_slot:
            valid_move = False
        if self.get_grid(to_type)[to_slot] is not None:
            valid_move = False
        if to_type == 'tray':
            if chip not in self.chips_placed_this_turn:
                valid_move = False
                self.dispatcher.dispatch('cannot take chips from the board')
        if not self.chip_validator.validate_move(hovering_slot, [chip]):
            valid_move = False
        
        if valid_move:
            grid_type, slot = hovering_slot
        else:
            grid_type, slot = origin_pos

        self.get_grid(grid_type)[slot] = chip

        self.chip_validator.validate_current_state()

        if valid_move:
            self.move_manager.move_history.append({
                'action': f'place_on_{grid_type}',
                'chip': chip,
                'from': origin_pos,
                'to': (grid_type, slot)
            })

        if chip not in self.chips_placed_this_turn:
            self.chips_placed_this_turn.append(chip)

        

    def chip_picked_up(self, grid_type, slot):
        self.get_grid(grid_type)[slot] = None
        self.chip_validator.validate_current_state()

    def undo_last_move(self):
        if not self.move_history:
            print("No moves to undo.")
            return
        print('one undone')
        last_move = self.move_history.pop()
        action = last_move['action']

        if action == 'place_on_board':
            # Remove chip from board, return to origin
            _, to_coords = last_move['to']
            self.board_grid.slots[to_coords] = None
            if last_move['from'][0] == 'tray':
                self.tray_grid.slots[last_move['from'][1]] = last_move['chip']
            elif last_move['from'][0] == 'board':
                self.board_grid.slots[last_move['from'][1]] = last_move['chip']
        elif action == 'place_in_tray':
            _, to_coords = last_move['to']
            self.tray_grid.slots[to_coords] = None
            if last_move['from'][0] == 'tray':
                self.tray_grid.slots[last_move['from'][1]] = last_move['chip']
            elif last_move['from'][0] == 'board':
                self.board_grid.slots[last_move['from'][1]] = last_move['chip']
        elif action == 'place_multiple_chips':
            from_type, from_coords = last_move['to']    #from as in we're undoing from 
            to_type, to_coords = last_move['from']
            from_slots = self.board_grid.slots if from_type == 'board' else self.tray_grid.slots
            to_slots = self.board_grid.slots if to_type == 'board' else self.tray_grid.slots


            # print(from_coords)
            # print(last_move['chip'][0])
            for coord in from_coords:
                from_slots[coord] = None
            chips = [chip for chip in last_move['chip'] if chip is not None]
            for indx, chip in enumerate(chips):
                to_slots[to_coords[indx]] = chip
                

      