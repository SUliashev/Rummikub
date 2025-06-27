class GameRules:
    def __init__(self, players, chip_tracker, chip_validator):
        self.players = players
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator
        self.turn_counter = 0
        self.first_turn_points = {player: 0 for player in players}
        # ... other state as needed

    def can_end_turn(self, player):
        # Check if board is valid
        if not self.chip_validator.valid_move():
            return False, "Invalid board state"
        # First turn 30 points rule
        if not player.first_turn_completed:
            points = sum(chip.number for chip, _ in self.chip_tracker.chips_placed_this_turn if not chip.is_joker)
            if points < 30:
                return False, "You must place at least 30 points on your first turn."
        # ... other rules
        player.first_turn_completed = True
        return True, ""


    def on_chip_drawn(self, player):
        player.has_drawn_chip = True

    def can_draw_chip(self, player):
        return not player.has_drawn_chip

    def on_turn_end(self, player):
        player.reset_current_move()
        self.turn_counter += 1
        self.chip_tracker.chips_placed_this_turn.clear()
        self.chip_tracker.move_history.clear()

    # ... more methods for other rules