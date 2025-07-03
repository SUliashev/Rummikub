import pygame
from src.Config.config import C as C
from src.Core.chip_tracker import ChipTracker
from src.Core.event_dispatcher import EventDispatcher
from src.GameUI.drag_manager import DragManager

class PlayerInteraction:
    chip_tracker: ChipTracker
    dispatcher: EventDispatcher
    drag_manager: DragManager
    warning_window: bool
    mouse_x: int
    mouse_y: int
    next_player_turn_wait: bool

    def __init__(self,  chip_tracker: ChipTracker, dispatcher: EventDispatcher, drag_manager: DragManager):
        self.chip_tracker = chip_tracker
        self.dispatcher = dispatcher
        self.drag_manager = drag_manager
        self.warning_window = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.next_player_turn_wait = False


    def handle_event(self, event: pygame.event)-> None:
        LEFT = 1
        
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            mouse_x, mouse_y = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                self.mouse_button_down(mouse_x, mouse_y )

            elif event.type == pygame.MOUSEMOTION: 
                self.update_self_mouse_coordinates(event)
                self.drag_manager.choose_next_slots(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                self.drag_manager.mouse_button_up_actions(mouse_x, mouse_y )
        
        else:
            pass


    def mouse_button_down(self, mouse_x : int, mouse_y: int) -> None:
        self.handle_end_game_buttons(mouse_x, mouse_y)
        
        if self.next_player_turn_wait == True:
            self.handle_next_player_ready_button(mouse_x, mouse_y)
            return
        if self.warning_window == True:
            self.handle_warning_window(mouse_x, mouse_y)
        if self.hanlde_change_of_tray_grid(mouse_x, mouse_y):
            return
        if self.button_in_right_rect_pressed(mouse_x, mouse_y):
            return
        if self.handle_next_turn_button_pressed(mouse_x, mouse_y):
            return
        self.drag_manager.mouse_button_down_actions(mouse_x, mouse_y)


    def update_self_mouse_coordinates(self, event: pygame.event)-> None:
        mouse_x, mouse_y = event.pos
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y 
        

    def handle_end_game_buttons(self, mouse_x: int, mouse_y: int) -> bool:
        if self.chip_tracker.end_game == True:
            if pygame.Rect(C.exit_game_button).collidepoint(mouse_x, mouse_y):
                self.dispatcher.dispatch('Exit Game')
        return False
    
    
    def handle_next_player_ready_button(self, mouse_x: int, mouse_y:int) -> None:
        if self.next_player_turn_wait == True:
            if pygame.Rect(C.next_player_ready_button).collidepoint(mouse_x, mouse_y):
                self.next_player_turn_wait = False
         
         
    def handle_warning_window(self, mouse_x: int, mouse_y: int) -> None:
        if pygame.Rect(C.undo_cofirmation_button).collidepoint(mouse_x, mouse_y):
            self.dispatcher.dispatch('undo all moves')
        self.warning_window = False
        

    def hanlde_change_of_tray_grid(self, mouse_x: int, mouse_y: int) -> bool:
        if pygame.Rect(C.tray_up_button).collidepoint(mouse_x, mouse_y):
            self.chip_tracker.tray_grid.visible_row_start = max(
                0, self.chip_tracker.tray_grid.visible_row_start - 1)
            self.chip_tracker.tray_grid.update_visible_slot_coordinates()
            return True
        elif pygame.Rect(C.tray_down_button).collidepoint(mouse_x, mouse_y):
            max_start = C.tray_rows - self.chip_tracker.tray_grid.visible_rows
            self.chip_tracker.tray_grid.visible_row_start = min(
                max_start, self.chip_tracker.tray_grid.visible_row_start + 1)
            self.chip_tracker.tray_grid.update_visible_slot_coordinates()
            return True
        return False


    def button_in_right_rect_pressed(self, mouse_x : int, mouse_y: int) -> bool:
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
    
    
    def handle_next_turn_button_pressed(self, mouse_x: int, mouse_y: int) -> bool:
        if pygame.Rect(C.next_player_button[0]).collidepoint(mouse_x, mouse_y):
            self.dispatcher.dispatch('button next player pressed')
            return True
        return False















    
   



