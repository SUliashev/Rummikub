from src.Core.chip import Chip
from src.Core.chip_tracker import ChipTracker
from src.GameUI.drag_manager import DragManager
from src.Core.event_dispatcher import EventDispatcher

class ChipValidator:
    chip_tracker: ChipTracker
    drag_manager: DragManager
    dispatcher: EventDispatcher
    slots: dict[tuple[int, int], Chip]
    slots_on_board: dict[tuple[int, int], Chip]

    def __init__(self, chip_tracker: ChipTracker, drag_manager: DragManager, dispatcher: EventDispatcher):    
        self.chip_tracker = chip_tracker
        self.drag_manager = drag_manager
        self.dispatcher = dispatcher
    
        self.slots = {}
        self.slots_on_board = {}
        self.validate_current_state()
       

    def validate_current_state(self) -> bool:
        all_slots_valid = True
        self.slots_on_board = {}
        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            if item_in_slot is None:
                self.slots_on_board[(row, col)] = True
            else:
                if  len(self.get_validation_chips((row, col))) < 3:
                    self.slots_on_board[(row, col)] = False
                    all_slots_valid = False
                    continue
                self.slots_on_board[(row, col)] = self.validate_combination(self.get_validation_chips((row, col)))
                if self.slots_on_board[(row, col)] == False:
                    all_slots_valid = False
        return all_slots_valid


    def validate_move(self, hovering_slots: list[tuple[int, int]], chips: list[Chip]) -> bool:
        if hovering_slots[0] == 'tray':
            return True
        
        self.slots = {}

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            self.slots[(row, col)] = item_in_slot   # copy current game state

        if len(chips) == 1:
            hovering_slot = hovering_slots[1]
            slot_to_check = hovering_slot[0] if isinstance(hovering_slot, list) else hovering_slot
            chip_to_check = chips[0]
            if self.slots[slot_to_check] != None:
                return False
            self.slots[slot_to_check] = chip_to_check

        elif len(chips) > 1 and hovering_slots[0] == 'board':
            slots = hovering_slots[1]

            for indx, slot in enumerate(slots):
                if self.slots[slot] != None:
                    return False
                self.slots[slot] = chips[indx]
        
        valid_move = True
        for slot, item_in_slot in self.slots.items():
            if item_in_slot == None:
                continue
            else:
                if not self.validate_combination(self.get_validation_chips(slot, self.slots)):
                    valid_move = False
                    break
        
        self.slots = {}

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            self.slots[(row, col)] = item_in_slot   # return current game state

        return valid_move


    def validate_combination(self, chips: list[Chip]) -> bool:
        jokers = [chip for chip in chips if chip is not None and getattr(chip, 'is_joker', False)]
        non_jokers = [chip for chip in chips if chip is not None and not getattr(chip, 'is_joker', False)]
        if not non_jokers:
            return True
        
        # Check for same color, increasing numbers
        if all(chip.color == non_jokers[0].color for chip in non_jokers):

            combination_numbers = [
                chip.number if chip and not getattr(chip, 'is_joker', False) else None
                for chip in chips]
                                    
            next_check = None
            for number in combination_numbers:
                if number is None and next_check is None:        
                    continue
                if number and next_check is None:
                    next_check = number + 1
                    continue
                if number is None and next_check:
                    next_check += 1
                    continue
                if number == next_check:
                    next_check += 1
                else:
                    return False
            return True
                
        # Check for same number, different colors
        if all(chip.number == non_jokers[0].number for chip in non_jokers):
            colors = {chip.color for chip in non_jokers}
            return len(colors) + len(jokers) == len(chips)
     
        return False


    def get_total_points_of_combination(self, chips: list[Chip]) -> int:
        jokers = [chip for chip in chips if chip is not None and getattr(chip, 'is_joker', False)]
        non_jokers = [chip for chip in chips if chip is not None and not getattr(chip, 'is_joker', False)]

        if all(chip.color == non_jokers[0].color for chip in non_jokers):
            def get_list_of_numbers(chips, i):  
                output = []
                previous_number = None
                for number in chips:
                    if number is None and previous_number is None:          
                        output.append(None)
                    if number:
                        output.append(number)
                        previous_number = number
                        continue
                    if number is None and previous_number:
                        output.append(previous_number + i)
                        previous_number += i
                        continue
                return output
            combination_numbers = [chip.number if not chip.is_joker else None for chip in chips]
            chips_with_numbers = get_list_of_numbers(combination_numbers, 1)
            full_check = get_list_of_numbers(reversed(chips_with_numbers), -1)
            return sum(full_check)

        if all(chip.number == non_jokers[0].number for chip in non_jokers):
            total = non_jokers[0].number * (len(non_jokers) + len(jokers))
            return total


    def get_validation_chips(self, slot: tuple[int, int], grid: dict[tuple[int, int], Chip]=None) -> list[Chip]:
        if grid == None:
            grid = self.chip_tracker.board_grid.slots
        chips = []
        row, col = slot
        i = 1
        while grid.get((row, col - i)) is not None:
            chips.append(grid[(row, col - i)])
            i += 1
        chips = chips[::-1]
        chips.append(grid[(row,col)])
        i = 1
        while grid.get((row, col + i)) is not None:
            chips.append(grid[(row, col + i)])
            i += 1
        return chips
    



            
