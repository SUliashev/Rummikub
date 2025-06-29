class GameRules:
    def __init__(self, players, chip_tracker, chip_validator, move_manager, dispatcher):
        self.players = players
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator 
        self.move_manager = move_manager
        self.dispatcher = dispatcher
        self.turn_counter = 0
        self.first_turn_points = {player: 0 for player in players}
        # ... other state as needed

    def can_end_turn(self, player):

        print(self.move_manager.chips_placed_this_turn)
        if self.chip_validator.validate_current_state() == False:
            self.dispatcher.dispatch('error', message="Invalid board state")
            return False, "Invalid board state"
        if len(self.move_manager.chips_placed_this_turn) == 0 and self.move_manager.one_chip_drawn == False:
            self.dispatcher.dispatch('error', message='One chip must be drawn if a move cannot be made')
            return False, ''
        if not player.first_turn_completed:
            if self.validate_first_move() == True:
                player.first_turn_completed = True
            elif len(self.move_manager.chips_placed_this_turn) > 0:
                    self.dispatcher.dispatch('error', message="You must place at least 30 points on your first turn." )
                    return False, "You must place at least 30 points on your first turn."
        # ... other rules
        return True, ""

    def validate_first_move(self):
        chips_checked = []
        total_amount = 0
        for chip in self.move_manager.chips_placed_this_turn:
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

    def on_chip_drawn(self, player):
        player.has_drawn_chip = True

    def can_draw_chip(self, player):
        return not player.has_drawn_chip

    def on_turn_end(self, player):
      
        self.turn_counter += 1
     
        

    # ... more methods for other rules