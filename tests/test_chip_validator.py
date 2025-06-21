import unittest
from chip_validator import ChipValidator
from chip import Chip
from board_grid import BoardGrid
from tray_grid import TrayGrid
from dragging_chip import DraggingChip

class DummyChip:
    def __init__(self, number, color, is_joker=False):
        self.number = number
        self.color = color
        self.is_joker = is_joker

class ChipValidatorTestCase(unittest.TestCase):
    def setUp(self):
        self.board_grid = BoardGrid()
        self.tray_grid = TrayGrid()
        self.dragging_chip = DraggingChip()
        # Set up a dummy chip tracker with the required attributes
        class DummyChipTracker:
            pass
        self.chip_tracker = DummyChipTracker()
        self.chip_tracker.board_grid = self.board_grid
        self.chip_tracker.tray_grid = self.tray_grid
        self.chip_tracker.dragging_chip = self.dragging_chip
        self.chip_validator = ChipValidator(self.chip_tracker)

    def test_valid_run(self):
        # Place a valid run: 5-red, 6-red, 7-red
        self.board_grid.slots[(0,0)] = DummyChip(5, "red")
        self.board_grid.slots[(0,1)] = DummyChip(6, "red")
        self.board_grid.slots[(0,2)] = DummyChip(7, "red")
        chips = [
            self.board_grid.slots[(0,0)],
            self.board_grid.slots[(0,1)],
            self.board_grid.slots[(0,2)],
        ]
        self.assertTrue(self.validator.validate_combination(chips))

    def test_invalid_run(self):
        # Place an invalid run: 5-red, 7-red, 8-red (gap too big)
        self.board_grid.slots[(0,0)] = DummyChip(5, "red")
        self.board_grid.slots[(0,1)] = DummyChip(7, "red")
        self.board_grid.slots[(0,2)] = DummyChip(8, "red")
        chips = [
            self.board_grid.slots[(0,0)],
            self.board_grid.slots[(0,1)],
            self.board_grid.slots[(0,2)],
        ]
        self.assertFalse(self.validator.validate_combination(chips))

    def test_valid_group_with_joker(self):
        # Place a group: 5-red, 5-blue, joker
        self.board_grid.slots[(0,0)] = DummyChip(5, "red")
        self.board_grid.slots[(0,1)] = DummyChip(5, "blue")
        self.board_grid.slots[(0,2)] = DummyChip(None, None, is_joker=True)
        chips = [
            self.board_grid.slots[(0,0)],
            self.board_grid.slots[(0,1)],
            self.board_grid.slots[(0,2)],
        ]
        self.assertTrue(self.validator.validate_combination(chips))

if __name__ == '__main__':
    unittest.main()