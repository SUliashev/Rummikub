from src.Core.chip import Chip
from src.Config.config import Config

class TrayGrid:
    def __init__(self):
        self.slots = {}
        self.create_coordinates()


    def get_first_open_slot(self):
        for row in range(Config.tray_rows):
            for col in range(Config.tray_cols):
                if self.slots[(row, col)] is None:
                    return (row, col)
        raise ValueError('No empty trayslots available')
    

    def put_chip_in_tray_from_hidden(self, chip: Chip):
        try:
            row, col = self.get_first_open_slot()
            self.slots[(row, col)] = chip

        except ValueError as e:
            print('Chip cannot be placed in tray from hidden:', e)


    def create_coordinates(self):
        for row in range(Config.tray_rows):
            for col in range(Config.tray_cols):
                self.slots[(row, col)] = None
          




        

