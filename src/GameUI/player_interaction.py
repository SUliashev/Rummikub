import pygame
from src.Config.config import C as C

class PlayerInteraction:
    def __init__(self,  chip_tracker, chip_validator, dispatcher):
        self.chip_tracker = chip_tracker
        self.chip_validator = chip_validator
        self.dispatcher = dispatcher
        self.chip_being_dragged = False
        self.selecting_multiple_chips = False
        self.chip_tracker.dragging_multiple_chips = False
        self.dragging_multiple_chips = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_button_down(event)

        elif event.type == pygame.MOUSEMOTION: # this is currently fed through API
            mouse_x, mouse_y = event.pos
            self.dispatcher.dispatch('mouse_movement', mouse_x=mouse_x, mouse_y=mouse_y)
            # if self.selecting_multiple_chips:
            #     self.dispatcher.dispatch('selecting multiple slots',(mouse_x, mouse_y) )

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_button_up(event)


    def mouse_button_down(self, event):           # reworking due to dispatcher # currently checks a chip is in place
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
            
            if self.chip_tracker.selected_chips: # and self.chip_tracker.mouse_over_selected_chip(mouse_x, mouse_y):
                if self.chip_tracker.start_dragging_selected_chips(mouse_x, mouse_y):
                    return
                    # self.chip_being_dragged = True
                    # self.chip_tracker.selection_start = None
                    # self.dragging_multiple_chips = True
                #     self.chip_tracker.dragging_multiple_chips = True
                #     return
                # else:
                #     self.chip_being_dragged = False


            if self.is_mouse_over_slot(event):
                slot_selected, slot_type_selected = self.is_mouse_over_slot(event)
                if slot_type_selected == 'board':
                    for (row, col), (x, y) in C.board_slot_coordinates.items():
                        if self.chip_tracker.board_grid.slots[(row, col)]:
                            slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                            if slot_rect.collidepoint(mouse_x, mouse_y):
                                self.chip_being_dragged = True
                                self.dispatcher.dispatch('start dragging chip', slot_type=slot_type_selected, slot=slot_selected)
                                return
                            
                elif slot_type_selected == 'tray':
                    for (row, col), (x, y) in C.tray_slot_coordinates.items():
                        if self.chip_tracker.tray_grid.slots[(row, col)]:         #these checks seem redundant
                            slot_rect = pygame.Rect(x, y, C.chip_width, C.chip_height)
                            if slot_rect.collidepoint(mouse_x, mouse_y):
                                self.chip_being_dragged = True
                                self.dispatcher.dispatch('start dragging chip', slot_type=slot_type_selected, slot=slot_selected)
                                return
                        

            
            if not self.chip_tracker.dragging_chip.chips:
                starting_x_y = (mouse_x, mouse_y)
                self.selecting_multiple_chips = starting_x_y
                # self.dispatcher.dispatch('start selecting multiple slots', starting_x_y=starting_x_y )
                self.chip_tracker.select_multiple_slots(starting_x_y)
                self.selecting_multiple_chips = True

    def mouse_button_up(self, event):
        x_y = event.pos
        if self.chip_being_dragged and self.dragging_multiple_chips == False:
            self.dispatcher.dispatch('chip_drag_end')
            self.chip_being_dragged = False
        elif self.chip_tracker.select_multiple_slots:
            self.chip_tracker.multiple_slots_selected(x_y)
            self.selecting_multiple_chips = False
        if self.chip_tracker.dragging_multiple_chips == True:
            self.chip_tracker.place_dragging_chips()


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
        








    
   



