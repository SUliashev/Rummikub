class DraggingChip:
    def __init__(self):
        self.chips = []
        self.chips_to_left = None
        self.main_chip = None
        self.chips_to_right = None

    def clear(self):
        self.chips = []
        self.chips_to_left = []
        self.main_chip = None
        self.chips_to_right = []
