import pygame
from src.Config.config import C as C

class PlayerInteraction:
    def __init__(self,  chip_tracker, chip_validator, dispatcher):
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator
        self.dispatcher = dispatcher
        self.mouse_x = 0
        self.mouse_y = 0


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_button_down(event)

        elif event.type == pygame.MOUSEMOTION: 
            self.update_self_mouse_coordinates(event)
            if self.chip_tracker.dragging_one_chip:
                self.chip_tracker.on_choose_next_slot(*event.pos)
            elif self.chip_tracker.dragging_multiple_chips:
                self.chip_tracker.on_choose_next_slot(*event.pos)
                self.chip_tracker.choose_multiple_hovering_slots()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_button_up(event)


    def mouse_button_down(self, event):           
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if pygame.Rect(C.right_rect).collidepoint(mouse_x, mouse_y):
                for button_name, (x, y, w, h) in C.right_buttons.items():
                    button_rect = pygame.Rect(x, y, w, h)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        self.dispatcher.dispatch(f'button {button_name} pressed')
                        return
                    
            
            if pygame.Rect(C.next_player_button[0]).collidepoint(mouse_x, mouse_y):
                self.dispatcher.dispatch('button next player pressed')
                return
            
            if self.chip_tracker.selected_chips: 
                if self.chip_tracker.start_dragging_selected_chips(mouse_x, mouse_y):
                    return

            if self.is_mouse_over_slot(event):
                slot_selected, slot_type_selected = self.is_mouse_over_slot(event)
                if slot_type_selected == 'board':
                    slot_coordinates = C.board_slot_coordinates
                    grid = self.chip_tracker.board_grid.slots
                else:
                    slot_coordinates = C.tray_slot_coordinates
                    grid = self.chip_tracker.tray_grid.slots
                for (row, col), (x, y) in slot_coordinates.items():
                    if grid[(row, col)]:
                        slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                        if slot_rect.collidepoint(mouse_x, mouse_y):
                            self.chip_tracker.dragging_one_chip = True
                            self.chip_drag_start(slot_type_selected, slot_selected)
                            return
                            
                        
            if not self.chip_tracker.dragging_chip.chips:
                self.chip_tracker.select_multiple_slots(mouse_x, mouse_y)
             

    def chip_drag_start(self, slot_type, slot):
        if slot_type == 'tray':
            if self.chip_tracker.tray_grid.slots[slot]:
                self.chip_tracker.chip_from_tray_to_dragging(slot)
                # self.chip_validator.validate_dragging_chip()
                
        elif slot_type == 'board':
            if self.chip_tracker.board_grid.slots[slot]:
                self.chip_tracker.chip_from_board_to_dragging(slot)
                # self.chip_validator.validate_dragging_chip()
                # self.chip_validator.validate_current_state()  


    def mouse_button_up(self, event):
        x_y = event.pos
        if self.chip_tracker.dragging_one_chip: 
            self.chip_drag_end()
            return
        
        elif self.chip_tracker.dragging_multiple_chips: # to add event dispatcher for validation
            self.multiple_chip_drag_end()
            return
  
        if self.chip_tracker.selection_start:
            self.chip_tracker.multiple_slots_selected(x_y)

    def chip_drag_end(self):
        next_slot = self.chip_tracker.hovering_slot
        if next_slot == None:
            self.chip_tracker.return_chip_to_origin_pos()
            self.chip_validator.validate_current_state()
        elif next_slot[0] == 'board':
            valid = self.chip_validator.valid_move()
            if valid:
                self.chip_tracker.chip_from_dragging_to_board(next_slot[1])
                self.chip_validator.validate_current_state()
            else:
                self.chip_tracker.return_chip_to_origin_pos()
                self.chip_validator.validate_current_state()
 
        elif next_slot[0] == 'tray':
            self.chip_tracker.chip_from_dragging_to_tray(next_slot[1])
         
        else:
            print('error with releasing chip')

    def multiple_chip_drag_end(self):
        if self.chip_tracker.multiple_hovering_slots:
            valid = self.chip_validator.valid_move()
            if valid:
                self.chip_tracker.place_multiple_chips_in_slots()
                self.chip_validator.validate_current_state()
            else:
                self.chip_tracker.return_multiple_chips_to_original_pos()
                self.chip_validator.validate_current_state()
        else:
            self.chip_tracker.return_multiple_chips_to_original_pos()
            self.chip_validator.validate_current_state()


    def is_mouse_over_slot(self, event):
        mouse_x, mouse_y = event.pos
        if self.is_mouse_over_board(event):
            for (row, col), (x, y) in C.board_slot_coordinates.items():
                slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    return ((row, col), 'board')
        if self.is_mouse_over_tray(event):
            for (row, col), (x, y) in C.tray_slot_coordinates.items():
                slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    return ((row, col), 'tray')
        return False
    

    def is_mouse_over_board(self, event):
        mouse_x, mouse_y = event.pos
        y_correct = mouse_y < C.tray_background_y
        return y_correct
       

    def is_mouse_over_tray(self, event):
        mouse_x, mouse_y = event.pos
        tray_rect = pygame.Rect(C.tray_background_x, C.tray_background_y, C.tray_background_width, C.tray_background_height)
        return tray_rect.collidepoint(mouse_x, mouse_y)


    def update_self_mouse_coordinates(self, event):
        mouse_x, mouse_y = event.pos
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y 
        








    
   



