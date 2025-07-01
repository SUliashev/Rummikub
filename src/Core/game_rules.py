class GameRules:
    def __init__(self, current_player, chip_tracker, chip_validator, move_manager, dispatcher):
        self.current_player = current_player
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator 
        self.move_manager = move_manager
        self.dispatcher = dispatcher
        self.turn_counter = 0
        self.subscribe_events()


    def subscribe_events(self):
        self.dispatcher.subscribe('button next player pressed', self.can_end_turn)


    def can_end_turn(self):
        if self.chip_validator.validate_current_state() == False:
            self.dispatcher.dispatch('error', message="Invalid board state")
            return False
        if len(self.move_manager.chips_placed_this_turn) == 0 and self.move_manager.one_chip_drawn == None:
            self.dispatcher.dispatch('error', message='One chip must be drawn if a move cannot be made')
            return False
        if not self.current_player.first_turn_completed:
            if self.validate_first_move() == True:
                self.current_player.first_turn_completed = True
            elif len(self.move_manager.chips_placed_this_turn) > 0:
                    self.dispatcher.dispatch('error', message="You must place at least 30 points on your first turn." )
                    return False
        if self.game_won() == True:
            self.chip_tracker.end_game = True
            self.dispatcher.dispatch('end of game')
            return
        self.dispatcher.dispatch('next player turn')


    def validate_first_move(self):
        if len(self.move_manager.chips_placed_this_turn) == 0:
            return False
        chips_checked = []
        total_amount = 0
        for chip in self.move_manager.chips_placed_this_turn:
            print(f'validation chip: {chip}')
            if chip not in chips_checked:
                slot = self.chip_tracker.get_position_of_chip(chip)
                chips_in_combination = self.chip_validator.get_validation_chips(slot)
                total_amount += self.chip_validator.get_total_points_of_combination(chips_in_combination)
                for chip in chips_in_combination:
                    chips_checked.append(chip)
        if total_amount >= 30:
            return True
        else:
            return False


    def on_turn_end(self, player):
        self.turn_counter += 1
     

    def game_won(self):
            for slot, chip in self.chip_tracker.tray_grid.slots.items():
                if chip is not None:
                    return False
            return True
    
