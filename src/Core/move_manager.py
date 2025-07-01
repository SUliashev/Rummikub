class MoveManager:
    def __init__(self, chip_tracker, chip_validator, dispatcher):
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator
        self.dispatcher = dispatcher
        self.move_history = []
        self.chips_placed_this_turn = set()
        self.one_chip_drawn = False
        self.subscribe_events()
        
    def draw_one_chip(self):
        if self.one_chip_drawn == None:
            chip = self.chip_tracker.place_chip_in_tray_from_hidden()
            self.one_chip_drawn = chip
            self.move_history.append({
                'action': 'place_chip_from_hidden',
                'chip': chip,
                'from': 'tray',
                'to': 'tray'
            })
        else:
            self.dispatcher.dispatch('error', message="Only one chip can be drawn per turn")

    def get_grid(self, grid_type):
        return self.chip_tracker.board_grid.slots if grid_type == 'board' else self.chip_tracker.tray_grid.slots
    

    def place_multiple_chips_to(self, hovering_slots, chips, origin_pos):
        if hovering_slots:
            valid_move = True
            if hovering_slots[0] == None:
                valid_move = False
            if not self.chip_validator.validate_move(hovering_slots, chips):
                valid_move = False
            if valid_move == True:
                if hovering_slots[0] == 'tray' and origin_pos[0] == 'board':
                    for chip in chips:
                        if chip not in self.chips_placed_this_turn:
                            valid_move =False
                            break
        else:
            valid_move = False

        if not valid_move:
            # Restore chips to their original positions
            origin_grid_type, origin_slots = origin_pos
            origin_grid = self.get_grid(origin_grid_type)
            for idx, chip in enumerate(chips):
                if chip is not None:
                    origin_grid[origin_slots[idx]] = chip
            self.dispatcher.dispatch('error', message="Cannot place chip here")
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
     
            for indx, chip in enumerate(chip for chip in chips if chip is not None):
                grid_slots[target_slots[indx]] = chip

            if grid_type == 'board' and origin_pos[0] == 'tray':
                for chip in chips:
                    if chip is not None:
                        self.chips_placed_this_turn.add(chip)
            elif grid_type == 'tray':
                for chip in chips:
                    if chip is not None:
                        self.chips_placed_this_turn.discard(chip)
            self.chip_validator.validate_current_state()

    def move_single_chip_to(self, hovering_slot, chip, origin_pos):
        valid_move = True
        if hovering_slot is not None and hovering_slot[1] is not None:
            to_type, to_slot = hovering_slot
            from_type, from_slot = origin_pos

            if self.get_grid(to_type)[to_slot] is not None:
                valid_move = False
            if to_type == 'tray' and from_type == 'board':
                if chip not in self.chips_placed_this_turn:
                    valid_move = False
            if not self.chip_validator.validate_move(hovering_slot, [chip]):
                valid_move = False
            
            if valid_move:
                grid_type, slot = hovering_slot
            else:
                grid_type, slot = origin_pos
                valid_move = False 
        else:
            grid_type, slot = origin_pos
            valid_move = False

        self.get_grid(grid_type)[slot] = chip
        if valid_move == True:
            self.chip_validator.validate_current_state()

        if valid_move == True:
            self.move_history.append({
                'action': f'place_on_{grid_type}',
                'chip': chip,
                'from': origin_pos,
                'to': (grid_type, slot)
            })
        
        if valid_move == False:
            self.dispatcher.dispatch('error', message="Cannot place chips here")

        if grid_type == 'board' and origin_pos[0] == 'tray':
                    self.chips_placed_this_turn.add(chip)
        elif grid_type == 'tray':
                    self.chips_placed_this_turn.discard(chip)
        


    def multiple_chips_picked_up(self, grid_type, chip_positions):
        for slot in chip_positions:
            self.get_grid(grid_type)[slot] = None
    
    def chip_picked_up(self, grid_type, slot):
        self.get_grid(grid_type)[slot] = None


    def undo_last_move(self):
        if not self.move_history:
            self.dispatcher.dispatch('error', message="No moves to be undone")
            return
        last_move = self.move_history.pop()
        action = last_move['action']

        draw_chip_factor = True
        if self.chip_tracker.get_position_in_tray(self.one_chip_drawn) is not None:
            drawn_chip_slot = self.chip_tracker.get_position_in_tray(self.one_chip_drawn)
            self.get_grid('tray')[drawn_chip_slot] = None
        else:
            draw_chip_factor = False

        if action in ['place_on_board', 'place_on_tray']:
            to_grid_type, from_coords = last_move['to']
            from_grid_type, to_coords = last_move['from']
            self.get_grid(to_grid_type)[from_coords] = None
            self.get_grid(from_grid_type)[to_coords] = last_move['chip']
            if to_grid_type == 'board' and from_grid_type == 'tray':
                if last_move['chip'] in self.chips_placed_this_turn:
                    self.chips_placed_this_turn.discard(last_move['chip'])
            elif to_grid_type == 'tray' and from_grid_type == 'board':
                if last_move['chip'] not in self.chips_placed_this_turn:
                    self.chips_placed_this_turn.add(last_move['chip'])
            
            self.chip_validator.validate_current_state()

        elif action == 'place_multiple_chips':
            to_grid_type, to_coords = last_move['to']    
            from_grid_type, from_coords = last_move['from']

            for coord in to_coords:
                self.get_grid(to_grid_type)[coord] = None
            chips = last_move['chip']
            for indx, chip in enumerate(chips):
                self.get_grid(from_grid_type)[from_coords[indx]] = chip
            if to_grid_type == 'board' and from_grid_type == 'tray':
                for chip in chips:
                    if chip in self.chips_placed_this_turn and chip is not None:
                        self.chips_placed_this_turn.discard(chip)
            elif to_grid_type == 'tray' and from_grid_type == 'board':
                for chip in chips:
                    if chip not in self.chips_placed_this_turn and chip is not None:
                        self.chips_placed_this_turn.add(chip)
        
        
            self.chip_validator.validate_current_state()

        print(self.chips_placed_this_turn)

        if draw_chip_factor:
            if self.get_grid('tray')[drawn_chip_slot] == None:
                self.get_grid('tray')[drawn_chip_slot] = self.one_chip_drawn
            else:
                slot = self.chip_tracker.tray_grid.get_first_open_slot()
                self.get_grid('tray')[slot] = self.one_chip_drawn

        if action == 'place_chip_from_hidden':
            drawn_chip_slot = self.chip_tracker.get_position_in_tray(self.one_chip_drawn)
            self.get_grid('tray')[drawn_chip_slot] = None
            self.undo_last_move()
            if self.get_grid('tray')[drawn_chip_slot] == None:
                self.get_grid('tray')[drawn_chip_slot] = last_move['chip']
            else:
                slot = self.chip_tracker.tray_grid.get_first_open_slot()
                self.get_grid('tray')[slot] = last_move['chip']
                
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
        self.dispatcher.subscribe('button Draw Chip pressed', self.draw_one_chip)

    def end_turn(self):
        self.move_history.clear()
        self.chips_placed_this_turn.clear()
        self.one_chip_drawn = None