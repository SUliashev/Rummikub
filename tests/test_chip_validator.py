import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Core.chip_validator import ChipValidator
from src.Config.config import C
from src.Grids.board_grid import BoardGrid
from src.Grids.tray_grid import TrayGrid
from src.GameUI.dragging_chip import DraggingChip

class DummyChip:
    number: int
    color: str
    is_joker: bool
    
    def __init__(self, number: int, color: str, is_joker:bool=False):
        self.number = number
        self.color = color
        self.is_joker = is_joker

class ChipValidatorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        C.setup_config()
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

    def test_valid_run(self) -> bool:
        # Place a valid run: 5-red, 6-red, 7-red
        self.board_grid.slots[(0,0)] = DummyChip(5, "red")
        self.board_grid.slots[(0,1)] = DummyChip(6, "red")
        self.board_grid.slots[(0,2)] = DummyChip(7, "red")
        chips = [
            self.board_grid.slots[(0,0)],
            self.board_grid.slots[(0,1)],
            self.board_grid.slots[(0,2)],
        ]
        self.assertTrue(self.chip_validator.validate_combination(chips))


    def test_invalid_run(self) -> bool:
        # Place an invalid run: 5-red, 7-red, 8-red (gap too big)
        self.board_grid.slots[(0,0)] = DummyChip(5, "red")
        self.board_grid.slots[(0,1)] = DummyChip(7, "red")
        self.board_grid.slots[(0,2)] = DummyChip(8, "red")
        chips = [
            self.board_grid.slots[(0,0)],
            self.board_grid.slots[(0,1)],
            self.board_grid.slots[(0,2)],
        ]
        self.assertFalse(self.chip_validator.validate_combination(chips))

    def test_valid_group_with_joker(self) -> bool:
        # Place a group: 5-red, 5-blue, joker
        self.board_grid.slots[(0,0)] = DummyChip(5, "red")
        self.board_grid.slots[(0,1)] = DummyChip(5, "blue")
        self.board_grid.slots[(0,2)] = DummyChip(None, None, is_joker=True)
        chips = [
            self.board_grid.slots[(0,0)],
            self.board_grid.slots[(0,1)],
            self.board_grid.slots[(0,2)],
        ]
        self.assertTrue(self.chip_validator.validate_combination(chips))


    def test_valid_group_of_same_color_with_joker(self) -> bool:
    
        self.board_grid.slots[(0,0)] = DummyChip(11, "red")
        self.board_grid.slots[(0,1)] = DummyChip(13, "red")
        self.board_grid.slots[(0,2)] = DummyChip(None, None, is_joker=True)
        chips = [
            self.board_grid.slots[(0,0)],
            self.board_grid.slots[(0,1)],
            self.board_grid.slots[(0,2)],
        ]
        self.assertFalse(self.chip_validator.validate_combination(chips))

if __name__ == '__main__':
    unittest.main()