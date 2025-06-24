from src.Config.config import C

class BoardGrid:
    def __init__(self):
        self.slots = {}
        self.hovering_slot = None 
        self.create_slots()


    def create_slots(self):
        for row in range(C.board_rows):
            for col in range(C.board_cols):
                self.slots[(row, col)] = None


                