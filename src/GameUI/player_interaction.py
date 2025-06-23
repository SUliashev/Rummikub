import pygame
from src.Config.config import Config as C

class PlayerInteraction:
    def __init__(self,  chip_tracker, chip_validator, dispatcher):
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator
        self.dispatcher = dispatcher
        self.chip_being_dragged = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_button_down(event)
            # if self.next_player_button_interaction(event):
            #     print("button pressed")
            #     return 'next player'
        elif event.type == pygame.MOUSEMOTION: # this is currently fed through API
            mouse_x, mouse_y = event.pos
            self.dispatcher.dispatch('mouse_movement', mouse_x=mouse_x, mouse_y=mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP and self.chip_tracker.dragging_chip.chip is not None:
            self.release_chip()


    def mouse_button_down(self, event):           # reworking due to dispatcher # currently checks a chip is in place
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.is_mouse_over_board(event):
                for (row, col), (x, y) in C.board_slot_coordinates.items():
                    if self.chip_tracker.board_grid.slots[(row, col)]:
                        slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                        if slot_rect.collidepoint(mouse_x, mouse_y):
                            self.chip_being_dragged = True
                            self.dispatcher.dispatch('chip_drag_start', slot_type='board', slot=(row, col))
                            
                            return
            elif self.is_mouse_over_tray(event):

                for (row, col), (x, y) in C.tray_slot_coordinates.items():
                    if self.chip_tracker.tray_grid.slots[(row, col)]:
                        slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                        if slot_rect.collidepoint(mouse_x, mouse_y):
                            self.chip_being_dragged = True
                            self.dispatcher.dispatch('chip_drag_start', slot_type='tray', slot=(row, col))
                            return
                        
            # if self.draw_button_interaction(event):
            #     return
            # slot = self.is_mouse_over_slot(event)
            # if slot:
            #     self.pick_up_chip(event, slot)


    def release_chip(self):
        self.dispatcher.dispatch('chip_drag_end', slot_type='board')



    def is_mouse_over_slot(self, event):
        mouse_x, mouse_y = event.pos
        if self.is_mouse_over_board(event):
            for (row, col), (x, y) in C.board_slot_coordinates.items():
                slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    return (row, col)
        if self.is_mouse_over_tray(event):
            for (row, col), (x, y) in C.tray_slot_coordinates.items():
                slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    return (row, col)
        return False
    

    def is_mouse_over_board(self, event):
        mouse_x, mouse_y = event.pos
        y_correct = mouse_y < C.tray_background_y
        return y_correct
       

    def is_mouse_over_tray(self, event):
        mouse_x, mouse_y = event.pos
        tray_rect = pygame.Rect(C.tray_background_x, C.tray_background_y, C.tray_background_width, C.tray_background_height)
        return tray_rect.collidepoint(mouse_x, mouse_y)


    def draw_button_interaction(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_rect = pygame.Rect(C.draw_button_x, C.draw_button_y, C.right_buttons_width, C.right_buttons_height)
            mouse_x, mouse_y = event.pos
            if button_rect.collidepoint(mouse_x, mouse_y):
                self.chip_tracker.place_chip_in_tray_from_hidden()
                return True
            

    def next_player_button_interaction(self, event):        # This can be improved
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_rect = pygame.Rect(C.next_player_button_x, C.next_player_button_y, C.right_buttons_width, C.right_buttons_height)
            mouse_x, mouse_y = event.pos
            if button_rect.collidepoint(mouse_x, mouse_y):
                return True
            return False
        








    
   



