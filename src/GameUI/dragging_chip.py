from src.Core.chip import Chip
class DraggingChip:
    chips: list[Chip]
    chips_to_left: list[Chip]
    main_chip: Chip
    chips_to_right: list[Chip]
    
    def __init__(self):
        self.chips = []
        self.chips_to_left = None
        self.main_chip = None
        self.chips_to_right = None

    def clear(self) -> None:
        self.chips = []
        self.chips_to_left = []
        self.main_chip = None
        self.chips_to_right = []

    def set_one_chip(self, chip: Chip) -> None:
        self.chips = [chip]
        self.chips_to_left = None
        self.main_chip = chip
        self.chips_to_right = None