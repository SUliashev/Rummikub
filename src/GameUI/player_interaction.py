import pygame
from src.Config.config import C as C

class PlayerInteraction:
    def __init__(self,  chip_tracker, chip_validator, dispatcher, move_manager, drag_manager):
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator
        self.dispatcher = dispatcher
        self.move_manager = move_manager
        self.drag_manager = drag_manager
        self.mouse_x = 0
        self.mouse_y = 0

    def mouse_button_down(self, mouse_x : int, mouse_y: int):
        if self.button_in_right_rect_pressed(mouse_x, mouse_y):
            return
        
        if self.handle_next_turn_button_pressed(mouse_x, mouse_y):
            return
        
        slot_type, slot = self.is_mouse_over_slot(mouse_x, mouse_y)
        chip = self.chip_tracker.get_chip_at(slot_type, slot)
        if chip:
            if self.drag_manager.selected_chips:
                self.drag_manager.start_dragging_selected_chips(chip)
            else:
                self.drag_manager.start_dragging_chip(slot_type, slot, chip)
        else:
            self.drag_manager.select_multiple_slots()

    def mouse_button_up(self, mouse_x: int, mouse_y: int):
        if self.drag_manager.dragging_one_chip: 
            self.drag_manager.chip_from_dragging_to_grid()
            return
        
        elif self.drag_manager.dragging_multiple_chips: # to add event dispatcher for validation
            self.multiple_chip_drag_end()
            return
  
        if self.chip_tracker.selection_start:
            self.chip_tracker.multiple_slots_selected((mouse_x, mouse_y))


        
    def handle_event(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            mouse_x, mouse_y = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_down(mouse_x, mouse_y )

            elif event.type == pygame.MOUSEMOTION: 
                self.update_self_mouse_coordinates(event)
                self.drag_manager.choose_next_slots(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_up(mouse_x, mouse_y )
        
        else:
            pass


    def handle_next_turn_button_pressed(self, mouse_x: int, mouse_y: int) -> bool:
        if pygame.Rect(C.next_player_button[0]).collidepoint(mouse_x, mouse_y):
            self.dispatcher.dispatch('button next player pressed')
            return True
        return False
        


    def button_in_right_rect_pressed(self, mouse_x : int, mouse_y: int):
        if pygame.Rect(C.right_rect).collidepoint(mouse_x, mouse_y):
            for button_name, (x, y, w, h) in C.right_buttons.items():
                button_rect = pygame.Rect(x, y, w, h)
                if button_rect.collidepoint(mouse_x, mouse_y):
                    self.dispatcher.dispatch(f'button {button_name} pressed')
                    return True
        return False
        


    def is_mouse_over_slot(self, mouse_x, mouse_y ):
        if self.is_mouse_over_board(mouse_x, mouse_y):
            for (row, col), (x, y) in C.board_slot_coordinates.items():
                slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    return ('board', (row, col))
        if self.is_mouse_over_tray(mouse_x, mouse_y):
            for (row, col), (x, y) in C.tray_slot_coordinates.items():
                slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    return ( 'tray', (row, col))
        return False


    def is_mouse_over_board(self, mouse_x, mouse_y):
        y_correct = mouse_y < C.tray_background_y
        return y_correct
       

    def is_mouse_over_tray(self, mouse_x, mouse_y):
        tray_rect = pygame.Rect(C.tray_background_x, C.tray_background_y, C.tray_background_width, C.tray_background_height)
        return tray_rect.collidepoint(mouse_x, mouse_y)







    








    # def mouse_button_down(self, event):           
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         mouse_x, mouse_y = event.pos
    #         if self.chip_tracker.undo_warning_window:
    #             if pygame.Rect(C.undo_cofirmation_button).collidepoint(mouse_x, mouse_y):
    #                 self.chip_tracker.undo_all_moves()
    #                 self.chip_validator.validate_current_state()


    #         if pygame.Rect(C.right_rect).collidepoint(mouse_x, mouse_y):
    #             for button_name, (x, y, w, h) in C.right_buttons.items():
    #                 button_rect = pygame.Rect(x, y, w, h)
    #                 if button_rect.collidepoint(mouse_x, mouse_y):
    #                     self.dispatcher.dispatch(f'button {button_name} pressed')
    #                     return
                    
            
    #         if pygame.Rect(C.next_player_button[0]).collidepoint(mouse_x, mouse_y):
    #             self.dispatcher.dispatch('button next player pressed')
    #             return
            
    #         if self.chip_tracker.selected_chips: 
    #             if self.chip_tracker.start_dragging_selected_chips(mouse_x, mouse_y):
    #                 return

    #         if self.is_mouse_over_slot(event):
    #             slot_selected, slot_type_selected = self.is_mouse_over_slot(event)
    #             if slot_type_selected == 'board':
    #                 slot_coordinates = C.board_slot_coordinates
    #                 grid = self.chip_tracker.board_grid.slots
    #             else:
    #                 slot_coordinates = C.tray_slot_coordinates
    #                 grid = self.chip_tracker.tray_grid.slots
    #             for (row, col), (x, y) in slot_coordinates.items():
    #                 if grid[(row, col)]:
    #                     slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
    #                     if slot_rect.collidepoint(mouse_x, mouse_y):
    #                         self.chip_tracker.dragging_one_chip = True
    #                         self.chip_drag_start(slot_type_selected, slot_selected)
    #                         return
                            
                        
    #         if not self.chip_tracker.dragging_chip.chips:
    #             self.chip_tracker.select_multiple_slots(mouse_x, mouse_y)
             






        # print('current state')
        # for slot, chip in self.chip_tracker.board_grid.slots.items():
        #     if chip is not None:
        #         print(f'{chip} on {slot}')




    




    def update_self_mouse_coordinates(self, event):
        mouse_x, mouse_y = event.pos
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y 
        








    
   



