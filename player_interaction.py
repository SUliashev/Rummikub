import pygame
from config import Config as C
from chip import Chip

class PlayerInteraction:
    def __init__(self,  chip_tracker):
        self.chip_tracker = chip_tracker

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pick_up_chip(event)
        # elif event.type == pygame.MOUSEMOTION and self.chip_tracker.dragging_chip.chip is not None:
            # self.choose_next_slot(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.release_chip(event)



    def pick_up_chip(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_mouse_over_slot(event):
                print('picked up')
                if self.is_mouse_over_tray(event):
                    self.chip_tracker.chip_from_tray_to_dragging(*self.is_mouse_over_slot(event))


    def choose_next_slot(self, event, snap_range=60):
        """
        Choose the nearest empty tray slot for the dragged chip within snap_range.
        Returns (row, col) if a slot is close enough and empty, else None.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        chip_center_x = mouse_x + C.chip_width // 2
        chip_center_y = mouse_y + C.chip_height // 2

        if self.is_mouse_over_board(event):
            slot_distances = []
            for (row, col), (slot_x, slot_y) in self.chip_tracker.board_grid.slot_coordinates.items():
                slot_center_x = slot_x + C.chip_width // 2
                slot_center_y = slot_y + C.chip_height // 2
                distance = int(((chip_center_x - slot_center_x) ** 2 + (chip_center_y - slot_center_y) ** 2) ** 0.5)
                print(distance)
                if distance <= snap_range and self.chip_tracker.board_grid.slots((row, col)) is None:
                    slot_distances.append((distance, (row, col)))
                
            slot_distances.sort(key=lambda x: x[0])
            if slot_distances:
                next_slot = slot_distances[0][1]
                return ('board', next_slot)
        
        elif self.is_mouse_over_tray(event):
            slot_distances = []
            for (row, col), (slot_x, slot_y) in self.chip_tracker.tray_grid.slot_coordinates.items():
                slot_center_x = slot_x + C.chip_width // 2
                slot_center_y = slot_y + C.chip_height // 2
                distance = int(((chip_center_x - slot_center_x) ** 2 + (chip_center_y - slot_center_y) ** 2) ** 0.5)
                if distance <= snap_range and self.chip_tracker.tray_grid.slots((row, col)) is None:
                    slot_distances.append((distance, (row, col)))
                
            slot_distances.sort(key=lambda x: x[0])
            next_slot = slot_distances[0][1]
            if slot_distances:
                    return ('tray', next_slot)         

        return None

    def release_chip(self, event):
        next_slot = self.choose_next_slot(event)
        if next_slot == None:
            self.chip_tracker.return_chip_to_origin_pos()
        elif next_slot[0] == 'board':
            self.chip_tracker.chip_from_dragging_to_board(next_slot[1])
        elif next_slot[0] == 'tray':
            self.chip_tracker.chip_from_dragging_to_tray(next_slot[1])
        else:
            print('error with releasing chip')

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
    
   

    # def snap_chip_to_nearby_slot(self):


        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if self.is_mouse_over_tray():
        #         # Check tray chips only
        #         for chip in self.chip_tracker.chips:
        #             if chip and chip.x_line[0] <= mouse_pos[0] <= chip.x_line[1] and chip.y_line[0] <= mouse_pos[1] <= chip.y_line[1]:
        #                 self.chip_tracker.remove_chip(chip)
        #                 self.dragging_chip = True

        # print("cannot pick up chip, error 'pick_up_chip' in PI")



    # def is_mouse_over_tray(self):
    #     mouse_x, mouse_y = pygame.mouse.get_pos()
    #     tray_rect = pygame.Rect(self.tray.x, self.tray.y, self.tray.width, self.tray.height)
    #     return tray_rect.collidepoint(mouse_x, mouse_y)
    

    
    # def drag_chip(self, event):
    #     if self.dragging_chip:
    #         if event.type == pygame.MOUSEMOTION:
    #             mouse_x, mouse_y = pygame.mouse.get_pos()
    #             self.chip_tracker.drag_chip(mouse_x, mouse_y)

    # def release_chip(self, event):
    #     if self.dragging_chip:
    #         if event.type == pygame.MOUSEBUTTONUP:
    #             mouse_x, mouse_y = pygame.mouse.get_pos()
    #             if self.is_mouse_over_tray():
    #                 tray_slot = self.chip_tracker.choose_next_tray_slot(mouse_x, mouse_y)
    #                 if tray_slot:
    #                     self.chip_tracker.snap_chip_to_tray_slot(tray_slot)
    #             else:
    #                 board_slot = self.chip_tracker.choose_next_slot(mouse_x, mouse_y)
    #                 if board_slot:
    #                     self.chip_tracker.snap_chip_to_board_slot(board_slot)
    #             self.dragging_chip = False
