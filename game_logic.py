class GameLogic:
    def __init__(self):
        self.board_slots = {slot_id: None for slot_id in range(120)}  # 120 slots

    def is_valid_combination(self, chips):
        """
        Check if a set of chips forms a valid combination (run or group).
        """
        if len(chips) < 3:
            return False

        # Check for a run (same color, consecutive numbers)
        if all(chip.color == chips[0].color for chip in chips):
            numbers = sorted(chip.number for chip in chips)
            return all(numbers[i] + 1 == numbers[i + 1] for i in range(len(numbers) - 1))

        # Check for a group (same number, different colors)
        if all(chip.number == chips[0].number for chip in chips):
            colors = {chip.color for chip in chips}
            return len(colors) == len(chips)

        return False

    def place_chip(self, chip, slot_id):
        """
        Place a chip in a slot and validate the move.
        """
        self.board_slots[slot_id] = chip

    def validate_board(self):
        """
        Validate all combinations on the board.
        """
        # Group chips by rows or columns and validate each group
        pass