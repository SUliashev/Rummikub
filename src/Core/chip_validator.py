class ChipValidator:
    def __init__(self, chip_tracker, dispatcher):    
        self.chip_tracker = chip_tracker
        self.dispatcher = dispatcher
        self.slots = {}
        self.slots_on_board = {}
        self.slot_next_to_chip = {}
        self.validate_current_state()
        self.subscribe_events()

    def validate_current_state(self):
        self.slots_on_board = {}

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            if item_in_slot is None:
                self.slots_on_board[(row, col)] = True
            else:
                if len(self.get_validation_chips(row, col)) == 1 or len(self.get_validation_chips(row, col)) < 3:
                    self.slots_on_board[(row, col)] = False
                    continue
                self.slots_on_board[(row, col)] = self.validate_combination(self.get_validation_chips(row, col))

    def valid_move(self):
        self.slots = {}

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            self.slots[(row, col)] = item_in_slot   # copy current game state

        if self.chip_tracker.dragging_one_chip == True:
            slot_to_check = self.chip_tracker.hovering_slot[1]
            chip_to_check = self.chip_tracker.dragging_chip.main_chip
            if self.slots[slot_to_check] != None:
                return False
            self.slots[slot_to_check] = chip_to_check

        elif self.chip_tracker.dragging_multiple_chips == True and self.chip_tracker.multiple_hovering_slots[0] == 'board':
            chips = self.chip_tracker.dragging_chip.chips
            slots = self.chip_tracker.multiple_hovering_slots[1]

            for indx, slot in enumerate(slots):
                if self.slots[slot] != None:
                    return False
                self.slots[slot] = chips[indx]
                

        for slot, item_in_slot in self.slots.items():
            if not item_in_slot:
                continue
            else:
                if not self.validate_combination(self.get_validation_chips(*slot)):
                    return False
        return True



    def validate_dragging_chip(self):
        self.slots = {}
        self.slot_next_to_chip = {}

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():

            if item_in_slot is not None:
                self.slots[(row, col)] = False
                continue

            self.slot_next_to_chip[(row, col)] = False
            valid = True

            chip_to_right = self.chip_tracker.board_grid.slots.get((row, col + 1))
            if chip_to_right:
                self.slot_next_to_chip[(row, col)] = True
                if not self.validate_combination(self.get_validation_chips(row, col)):
                    valid = False

            chip_to_left = self.chip_tracker.board_grid.slots.get((row, col - 1))
            if chip_to_left:
                self.slot_next_to_chip[(row, col)] = True
                if not self.validate_combination(self.get_validation_chips(row, col)):
                    valid = False

            self.slots[(row, col)] = valid


    def validate_dragging_chip(self):
        self.slots = {}
        self.slot_next_to_chip = {}

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():

            if item_in_slot is not None:
                self.slots[(row, col)] = False
                continue

            self.slot_next_to_chip[(row, col)] = False
            valid = True

            chip_to_right = self.chip_tracker.board_grid.slots.get((row, col + 1))
            if chip_to_right:
                self.slot_next_to_chip[(row, col)] = True
                if not self.validate_combination(self.get_validation_chips(row, col)):
                    valid = False

            chip_to_left = self.chip_tracker.board_grid.slots.get((row, col - 1))
            if chip_to_left:
                self.slot_next_to_chip[(row, col)] = True
                if not self.validate_combination(self.get_validation_chips(row, col)):
                    valid = False

            self.slots[(row, col)] = valid
 
 

    def validate_combination(self, chips):
        jokers = [chip for chip in chips if getattr(chip, 'is_joker', False)]
        non_jokers = [chip for chip in chips if not getattr(chip, 'is_joker', False)]
        if not non_jokers:
            return True
        # Check for same color, increasing numbers
        if all(chip.color == non_jokers[0].color for chip in non_jokers):

            combination_numbers = [chip.number if not chip.is_joker else None for chip in chips]
            next_check = None
            for number in combination_numbers:
                if number is None and next_check is None:          #  None, 12 , None,  13
                    continue
                if number and next_check is None:
                    next_check = number + 1
                    continue
                if number is None and next_check:
                    next_check += 1
                    continue
                if number == next_check:
                    next_check += 1
                else:
                    return False
            return True
                

        # Check for same number, different colors
        if all(chip.number == non_jokers[0].number for chip in non_jokers):
            colors = {chip.color for chip in non_jokers}
            return len(colors) + len(jokers) == len(chips)
     
        return False
        

    def get_validation_chips(self, row, col):
        chips = []
        
        i = 1
        while self.slots.get((row, col - i)) is not None:
            chips.append(self.slots[(row, col - i)])
            i += 1
        chips = chips[::-1]
        chips.append(self.slots[(row,col)])
        i = 1
        while self.slots.get((row, col + i)) is not None:
            chips.append(self.slots[(row, col + i)])
            i += 1
        return chips

    def undo_move(self):
        self.chip_tracker.undo_last_move()
        self.validate_current_state()

        
    def subscribe_events(self):
        self.dispatcher.subscribe('button Undo Move pressed', self.undo_move)
       

    

    
