import pygame
from config import Config as C
from chip import Chip

class PlayerInteraction:
    def __init__(self,  chip_tracker, chip_validator):
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_button_down(event)
        elif event.type == pygame.MOUSEMOTION and self.chip_tracker.dragging_chip.chip is not None:
            self.choose_next_slot(event)
        elif event.type == pygame.MOUSEBUTTONUP and self.chip_tracker.dragging_chip.chip is not None:
            self.release_chip(event)


    def mouse_button_down(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.draw_button_interaction(event):
                return
            slot = self.is_mouse_over_slot(event)
            if slot:
                self.pick_up_chip(event, slot)

    def pick_up_chip(self, event, slot):
        if self.is_mouse_over_tray(event):
            if self.chip_tracker.tray_grid.slots[slot]:
                self.chip_tracker.chip_from_tray_to_dragging(slot)
                self.chip_validator.validate_current_state()
        elif self.is_mouse_over_board(event):
            if self.chip_tracker.board_grid.slots[slot]:
                self.chip_tracker.chip_from_board_to_dragging(slot)
                self.chip_validator.validate_current_state()

    def draw_button_interaction(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_rect = pygame.Rect(C.draw_button_x, C.draw_button_y, C.draw_button_width, C.draw_button_height)
            mouse_x, mouse_y = event.pos
            if button_rect.collidepoint(mouse_x, mouse_y):
                self.chip_tracker.place_chip_in_tray_from_hidden()
                return True
        
    def release_chip(self, event):
        next_slot = self.chip_tracker.hovering_slot
        if next_slot == None:
            self.chip_tracker.return_chip_to_origin_pos()
        elif next_slot[0] == 'board':
            self.chip_tracker.chip_from_dragging_to_board(next_slot[1])
 
        elif next_slot[0] == 'tray':
            self.chip_tracker.chip_from_dragging_to_tray(next_slot[1])
         
        else:
            print('error with releasing chip')

    def choose_next_slot(self, event, snap_range=60):
        """
        Snap the dragged chip to the nearest empty board or tray slot within snap_range.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        chip_center_x = mouse_x 
        chip_center_y = mouse_y 

        def find_nearest_empty_slot(slot_coordinates, slots_dict):
            slot_distances = []
            for (row, col), (slot_x, slot_y) in slot_coordinates.items():
                slot_center_x = slot_x + C.chip_width // 2
                slot_center_y = slot_y + C.chip_height // 2
                distance = int(((chip_center_x - slot_center_x) ** 2 + (chip_center_y - slot_center_y) ** 2) ** 0.5)
                if distance <= snap_range and slots_dict[(row, col)] is None:
                    slot_distances.append((distance, (row, col)))
            if slot_distances:
                slot_distances.sort(key=lambda x: x[0])
                return slot_distances[0][1]
            return None

        if self.is_mouse_over_board(event):
            next_slot = find_nearest_empty_slot(
                self.chip_tracker.board_grid.slot_coordinates,
                self.chip_tracker.board_grid.slots
            )
            if next_slot:
                self.chip_tracker.hovering_slot = ('board', next_slot)
                return

        elif self.is_mouse_over_tray(event):
            next_slot = find_nearest_empty_slot(
                self.chip_tracker.tray_grid.slot_coordinates,
                self.chip_tracker.tray_grid.slots
            )
            if next_slot:
                self.chip_tracker.hovering_slot = ('tray', next_slot)
                return

        self.chip_tracker.hovering_slot = None


    def is_mouse_over_board(self, event):
        mouse_x, mouse_y = event.pos
        y_correct = mouse_y < C.tray_background_y
        return y_correct
       
    def is_mouse_over_tray(self, event):
        mouse_x, mouse_y = event.pos
        tray_rect = pygame.Rect(C.tray_background_x, C.tray_background_y, C.tray_background_width, C.tray_background_height)
        return tray_rect.collidepoint(mouse_x, mouse_y)
        
    def is_mouse_over_slot(self, event):
        mouse_x, mouse_y = event.pos
        if self.is_mouse_over_board(event):
            for (row, col), (x, y) in self.chip_tracker.board_grid.slot_coordinates.items():
                slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    return (row, col)
        if self.is_mouse_over_tray(event):
            for (row, col), (x, y) in self.chip_tracker.tray_grid.slot_coordinates.items():
                slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    return (row, col)
        return False
    
   



