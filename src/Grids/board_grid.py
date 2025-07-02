from src.Config.config import C
from src.Core.chip import Chip

class BoardGrid:
    slots: dict[tuple[int, int], Chip]

    def __init__(self):
        self.slots = {}
        self.create_slots()


    def create_slots(self) -> None:
        for row in range(C.board_rows):
            for col in range(C.board_cols):
                self.slots[(row, col)] = None


                