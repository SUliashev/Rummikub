class MoveManager:
    def __init__(self, chip_tracker, chip_validator, dispatcher):
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator
        self.dispatcher = dispatcher
        self.move_history = []
        self.chips_placed_this_turn = []
        self.subscribe_events()
        


    def get_grid(self, grid_type):
        return self.chip_tracker.board_grid.slots if grid_type == 'board' else self.chip_tracker.tray_grid.slots
    

    def place_multiple_chips_to(self, hovering_slots, chips, origin_pos):
        valid_move = True
        if not self.chip_validator.validate_move(hovering_slots, chips):
            valid_move = False
        if valid_move == True:
            if hovering_slots[0] == 'tray':
                for chip in chips:
                    if chip not in self.chips_placed_this_turn:
                        valid_move =False
                        self.dispatcher.dispatch('cannot take chips from the board')
                        break

        if not valid_move:
            # Restore chips to their original positions
            origin_grid_type, origin_slots = origin_pos
            origin_grid = self.get_grid(origin_grid_type)
            for idx, chip in enumerate(chips):
                if chip is not None:
                    origin_grid[origin_slots[idx]] = chip
            self.chip_validator.validate_current_state()
            return
        
        else:
            grid_type, target_slots = hovering_slots
            grid_slots = self.get_grid(grid_type)

        
            self.move_history.append({
                'action': 'place_multiple_chips',
                'chip': chips,
                'from': origin_pos,
                'to': (grid_type, target_slots)
            })
            print(f'logger: origin pos: {origin_pos}, chips: {chips}')
            for indx, chip in enumerate(chip for chip in chips if chip is not None):
                grid_slots[target_slots[indx]] = chip

            if grid_type == 'board' and origin_pos[0] == 'tray':
                for chip in chips:
                    if chip not in self.chips_placed_this_turn:
                        self.chips_placed_this_turn.append(chip)
            elif grid_type == 'tray':
                for chip in chips:
                    if chip in self.chips_placed_this_turn:
                        self.chips_placed_this_turn.remove(chip)

            self.chip_validator.validate_current_state()

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
            self.move_history.append({
                'action': f'place_on_{grid_type}',
                'chip': chip,
                'from': origin_pos,
                'to': (grid_type, slot)
            })

        if chip not in self.chips_placed_this_turn:
            self.chips_placed_this_turn.append(chip)

    def multiple_chips_picked_up(self, grid_type, chip_positions):
        for slot in chip_positions:
            self.get_grid(grid_type)[slot] = None
        self.chip_validator.validate_current_state()

    def chip_picked_up(self, grid_type, slot):
        # print(f'subs: gird_type = {grid_type}, slot = {slot}')
        self.get_grid(grid_type)[slot] = None
        self.chip_validator.validate_current_state()


    def undo_last_move(self):
        if not self.move_history:
            print("No moves to undo.")
            return
        print('one undone')
        last_move = self.move_history.pop()
        action = last_move['action']

        if action in ['place_on_board', 'place_on_tray']:
            to_grid_type, from_coords = last_move['to']
            from_grid_type, to_coords = last_move['from']
            self.get_grid(to_grid_type)[from_coords] = None
            self.get_grid(from_grid_type)[to_coords] = last_move['chip']
            if to_grid_type == 'board' and from_grid_type == 'tray':
                if last_move['chip'] in self.chips_placed_this_turn:
                    self.chips_placed_this_turn.remove(last_move['chip'])
            elif to_grid_type == 'tray' and from_grid_type == 'board':
                if last_move['chip'] not in self.chips_placed_this_turn:
                    self.chips_placed_this_turn.append(last_move['chip'])
            
            self.chip_validator.validate_current_state()

        elif action == 'place_multiple_chips':
            to_grid_type, to_coords = last_move['to']    #from as in we're undoing from 
            from_grid_type, from_coords = last_move['from']

            for coord in to_coords:
                self.get_grid(to_grid_type)[coord] = None
            chips = last_move['chip']
            for indx, chip in enumerate(chips):
                self.get_grid(from_grid_type)[from_coords[indx]] = chip
            if to_grid_type == 'board' and from_grid_type == 'tray':
                for chips in chips:
                    if chip in self.chips_placed_this_turn:
                        self.chips_placed_this_turn.remove(chip)
            elif to_grid_type == 'tray' and from_grid_type == 'board':
                for chip in chips:
                    if chip not in self.chips_placed_this_turn:
                        self.chips_placed_this_turn.append(chip)
        
            self.chip_validator.validate_current_state()
    
    def undo_all_moves(self):
        for i in range(len(self.move_history)):
            self.undo_last_move()
        self.undo_warning_window = False

    def subscribe_events(self):
        self.dispatcher.subscribe('chip_picked_up', self.chip_picked_up)
        self.dispatcher.subscribe('chip placed on slot', self.move_single_chip_to )
        self.dispatcher.subscribe('multiple chips picked up', self.multiple_chips_picked_up)
        self.dispatcher.subscribe('multiple chips placed', self.place_multiple_chips_to)
        self.dispatcher.subscribe('button Undo Move pressed', self.undo_last_move)
        self.dispatcher.subscribe('undo all moves', self.undo_all_moves)