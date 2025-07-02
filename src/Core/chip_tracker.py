from src.Core.chip import Chip
from src.Grids.board_grid import BoardGrid
from src.Grids.tray_grid import TrayGrid
from src.Core.event_dispatcher import EventDispatcher

class ChipTracker:
    board_grid: BoardGrid
    tray_grid: TrayGrid
    dispatcher: EventDispatcher
    hidden_chips: list[Chip]
    end_game:bool

    def __init__(self, board_grid: BoardGrid, tray_grid: TrayGrid, dispatcher: EventDispatcher):
        self.board_grid = board_grid
        self.tray_grid = tray_grid
        self.dispatcher = dispatcher
        self.hidden_chips = [] 
        self.end_game = False


    def get_chip_at(self, slot_type: str, slot: tuple[int, int]) -> dict[tuple[int, int], Chip]:
        grid_to_choose_from = self.board_grid.slots if slot_type == 'board' else self.tray_grid.slots
        return grid_to_choose_from[slot]


    def get_position_of_chip(self, search_chip: Chip) -> tuple[int, int]:
        for slot, chip in self.board_grid.slots.items():
            if chip == search_chip:
                return slot
        return None
        
    def get_position_in_tray(self, search_chip: Chip) -> tuple[int, int]:
        for slot, chip in self.tray_grid.slots.items():
            if chip == search_chip:
                return slot
        return None

    def place_chip_in_tray_from_hidden(self) -> Chip:
        if not self.hidden_chips:
            self.dispatcher.dispatch('error', 'No hidden chips left')
            return

        chip = self.hidden_chips.pop()
        self.tray_grid.put_chip_in_tray_from_hidden(chip)
        return chip


  



  





