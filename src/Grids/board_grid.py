from src.Config.config import Config

class BoardGrid:
    def __init__(self):
        self.slots = {}
        self.hovering_slot = None 
        self.create_slots()


    def create_slots(self):
        for row in range(Config.board_rows):
            for col in range(Config.board_cols):
                self.slots[(row, col)] = None


                