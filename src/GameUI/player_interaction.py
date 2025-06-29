import pygame
from src.Config.config import C as C

class PlayerInteraction:
    def __init__(self,  chip_tracker, dispatcher, drag_manager):
        self.chip_tracker = chip_tracker
        self.dispatcher = dispatcher
        self.drag_manager = drag_manager
        self.warning_window = False
        self.mouse_x = 0
        self.mouse_y = 0

    def mouse_button_down(self, mouse_x : int, mouse_y: int):
        if self.warning_window == True:
            self.handle_warning_window(mouse_x, mouse_y)

        if self.button_in_right_rect_pressed(mouse_x, mouse_y):
            return
        
        if self.handle_next_turn_button_pressed(mouse_x, mouse_y):
            return

        self.drag_manager.mouse_button_down_actions(mouse_x, mouse_y)


    def handle_warning_window(self, mouse_x, mouse_y):
        if pygame.Rect(C.undo_cofirmation_button).collidepoint(mouse_x, mouse_y):
            self.dispatcher.dispatch('undo all moves')
        self.warning_window = False
        
    def handle_event(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            mouse_x, mouse_y = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_down(mouse_x, mouse_y )

            elif event.type == pygame.MOUSEMOTION: 
                self.update_self_mouse_coordinates(event)
                self.drag_manager.choose_next_slots(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.drag_manager.mouse_button_up_actions(mouse_x, mouse_y )
        
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
                    if button_name == 'Undo All Moves':
                        self.warning_window = True
                        continue
                    self.dispatcher.dispatch(f'button {button_name} pressed')
                    return True
        return False
        










    








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
        








    
   



