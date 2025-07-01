from src.Core.chip import Chip
from src.Config.config import C

class TrayGrid:
    def __init__(self):
        self.slots = {}
        self.visible_row_start = 0  # Index of the first visible row
        self.visible_rows = 2
        self.create_coordinates()

    def update_visible_slot_coordinates(self):
        C.tray_slot_coordinates = {}
        start_row = self.visible_row_start
        print(self.visible_row_start)
        for visible_row in range(self.visible_rows):
            actual_row = start_row + visible_row
            for col in range(C.tray_cols):
                x = C.tray_grid_x + col * (C.chip_width + C.tray_slot_horizontal_spacing)
                y = C.tray_grid_y + visible_row * (C.chip_height + C.tray_slot_vertical_spacing)
                C.tray_slot_coordinates[(actual_row, col)] = (x, y)


    def get_first_open_slot(self):
        for row in range(C.tray_rows):
            for col in range(C.tray_cols):
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
        for row in range(C.tray_rows):
            for col in range(C.tray_cols):
                self.slots[(row, col)] = None
          

    def sort_chips_in_tray(self):
        all_chips_in_tray = [chip for chip in self.slots.values() if chip is not None]
        if all_chips_in_tray:
            sorted_chips = []

            colors = set(chip.color for chip in all_chips_in_tray if not chip.is_joker)
            jokers = [chip for chip in all_chips_in_tray if chip.is_joker]
            if colors:
                for color in colors:
                    chips_of_same_color = sorted(
                        [chip for chip in all_chips_in_tray if chip.color == color and not chip.is_joker], 
                        key=lambda chip: chip.number)
                    
                    sorted_chips += chips_of_same_color

            if jokers:
                sorted_chips += jokers

            for slot, chip in self.slots.items():
                self.slots[slot] = None
            for chip in sorted_chips:
                self.slots[self.get_first_open_slot()] = chip
                        





        

