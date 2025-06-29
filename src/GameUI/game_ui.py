import pygame
from src.Core.chip import Chip
from src.Config.config import C

class GameUI:
    def __init__(self, chip_tracker, chip_validator, current_player, dispatcher, player_interaction, drag_manager):
        self.window = C.window 
        print('size', self.window.get_size())
        pygame.display.set_caption("Rummikub")
        self.chip_tracker = chip_tracker  # Use ChipTracker for chip management
        self.drag_manager = drag_manager
        self.chip_validator = chip_validator
        self.current_player = current_player
        self.dispatcher = dispatcher
        self.player_interaction = player_interaction
        self.multiple_chips_dragged = False



    def draw_selection_rectangle(self):
        if self.drag_manager.selection_start:
            x1, y1 = self.drag_manager.selection_start
            x2 = self.player_interaction.mouse_x
            y2 = self.player_interaction.mouse_y
            rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill((0, 120, 255, 60))  
            self.window.blit(s, rect.topleft)
            pygame.draw.rect(self.window, (0, 120, 255), rect, 2)


    def draw(self):
        self.window.fill((39,105,127))  # Clear the screen

        self.draw_tray_background()
        self.draw_tray_grid()

        self.draw_next_player_button()

        self.draw_board_slots()
        self.draw_side_rectangle()
        self.draw_right_side_buttons()
        self.draw_incorrect_chip_combination()      # shows which combinations on the board are not valid
        self.draw_hovering_slot()
        self.draw_moving_chip()

        self.draw_selection_rectangle()
        self.show_selected_chips()
        self.draw_undo_all_confirmation()

    def show_selected_chips(self):
        if self.drag_manager.selected_chips:
            if not self.drag_manager.dragging_multiple_chips:
            
                if self.drag_manager.selected_chips[0] == 'tray':
                    slots_to_highlight = C.tray_slot_coordinates
                else:
                    slots_to_highlight = C.board_slot_coordinates
                (row_type, chip_positions, chips_in_row) = self.drag_manager.selected_chips
                for indx, chip in enumerate(chips_in_row):
                    if chip is not None:
                        self.draw_chip_hue(*slots_to_highlight[chip_positions[indx]])
        
    def draw_side_rectangle(self):
        pygame.draw.rect(
            self.window,
            (200, 200, 200),  # Rectangle color
            (C.right_rect),
            border_radius=12
        )

    def draw_right_side_buttons(self):
        for button_name, rect in C.right_buttons.items():
            pygame.draw.rect(
                self.window,
                (69, 69, 69),  # Button color
                rect,
                border_radius=8
        )
            font_size = C.right_buttons_font_size[button_name]
            font = pygame.font.SysFont(None, font_size)
            text = font.render(button_name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))

            self.window.blit(text, text_rect)



    def draw_board_slots(self):
        draw_numbers_next_to_slots = True       # testing stage, adds numbers next to the slots on the board
        font = pygame.font.SysFont(None, 18)

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            x , y = C.board_slot_coordinates[row, col]
            if item_in_slot is None:
                    self.draw_empty_slot(x, y)
            else:
                self.draw_chip(item_in_slot, x, y)
            
            if draw_numbers_next_to_slots:
                col_text = font.render(str(col + 1), True, (200, 200, 0))
                self.window.blit(col_text, (x + 4, y + 2))


    def draw_chip(self, chip, x, y):
        chip_drawing = self.window.blit(chip.sprite, (x, y))
        return chip_drawing
    
    
    def draw_empty_slot(self, x: int, y: int):
        border_radius = 9
        thickness = 2
        pygame.draw.rect(
        self.window, (255, 255, 255),
        (x, y, C.chip_width, C.chip_height),
        thickness, border_radius=border_radius)
        
        
    def draw_hovering_slot(self):
        if not self.drag_manager.hovering_slot:
            return
        
        if len(self.drag_manager.dragging_chip.chips) == 1:
            grid_type, slot = self.drag_manager.hovering_slot 
            if slot is None:
                return      
            grid_coord = C.tray_slot_coordinates if grid_type == 'tray' else C.board_slot_coordinates
            x, y = grid_coord[slot]
   

            border_radius = 9
            rect = pygame.draw.rect(
                    self.window, (0, 30, 140),
                    (x, y, C.chip_width, C.chip_height),
                    3, border_radius=border_radius)
    
        if self.drag_manager.dragging_multiple_chips:
            self.draw_multiple_hovering_slots()
        

    def draw_multiple_hovering_slots(self):
        if self.drag_manager.multiple_hovering_slots:
            slot_type , slots = self.drag_manager.multiple_hovering_slots
            if slot_type == 'tray':
                slot_coordinates = C.tray_slot_coordinates
            else:
                slot_coordinates = C.board_slot_coordinates
            border_radius = 9
            for row, col in slots:
                x,y = slot_coordinates[row, col]
                rect = pygame.draw.rect(
                    self.window, (0, 30, 140),
                    (x, y, C.chip_width, C.chip_height),
                    3, border_radius=border_radius)
        
        
    def draw_incorrect_chip_combination(self):
        for (row, col), correct in self.chip_validator.slots_on_board.items():
            if not correct:
                self.draw_invalid_placed_chip_border(*C.board_slot_coordinates[row, col])
                

    def draw_invalid_placed_chip_border(self, x, y):       
        thickness = 5
        border_radius = 15
        pygame.draw.rect(
        self.window, (255, 0, 0),
        (x - thickness , y - thickness , C.chip_width + thickness * 2, C.chip_height  + thickness * 2),
        thickness, border_radius=border_radius)
        
            
    def draw_chip_hue(self, x, y, width=None, height=None, outline_thickness=10, border_radius=10):
        if width is None:
            width = C.chip_width
        if height is None:
            height = C.chip_height

        rect_x = x - outline_thickness // 2
        rect_y = y - outline_thickness // 2
        rect_w = width + outline_thickness
        rect_h = height + outline_thickness

        outline_surface = pygame.Surface((rect_w, rect_h), pygame.SRCALPHA)
        pygame.draw.rect(
            outline_surface,
            (255, 255, 255, 120),  # White with alpha for soft glow
            (0, 0, rect_w, rect_h),
            border_radius=border_radius
        )
        self.window.blit(outline_surface, (rect_x, rect_y))


    def draw_moving_chip(self):
        if self.drag_manager.dragging_chip.main_chip:
            chips = self.drag_manager.dragging_chip.chips
            if len(chips) == 1 or chips is None:
                chip = self.drag_manager.dragging_chip.main_chip
                x = self.player_interaction.mouse_x - C.chip_width / 2
                y = self.player_interaction.mouse_y - C.chip_height / 2

                # Draw the hue behind the chip
                self.draw_chip_hue(x, y)

                # Draw the chip itself
                self.draw_chip(chip, x, y)
                return
            else:
                self.draw_multiple_moving_chips()
        

    def draw_multiple_moving_chips(self):
        dc = self.drag_manager.dragging_chip
        if not hasattr(dc, "main_chip") or dc.main_chip is None:
            return

        chip_w = C.chip_width
        chip_h = C.chip_height
        spacing = C.slot_horizontal_spacing

        mouse_x = self.player_interaction.mouse_x
        mouse_y = self.player_interaction.mouse_y

        for i, chip in enumerate(reversed(dc.chips_to_left)):
            if chip is None:
                continue
            x = mouse_x - chip_w // 2 - (chip_w + spacing) * (i + 1)
            y = mouse_y - chip_h // 2
            self.draw_chip_hue(x, y)
            self.draw_chip(chip, x, y)

        x_main = mouse_x - chip_w // 2
        y_main = mouse_y - chip_h // 2
        self.draw_chip_hue(x_main, y_main)
        self.draw_chip(dc.main_chip, x_main, y_main)

        for i, chip in enumerate(dc.chips_to_right):
            if chip is None:
                continue
            x = mouse_x + (chip_w + spacing) * (i + 1) - chip_w // 2
            y = mouse_y - chip_h // 2
            self.draw_chip_hue(x, y)
            self.draw_chip(chip, x, y)          
         
        
    def draw_next_player_button(self): #to update later with config data
        button_rect = pygame.Rect(C.next_player_button[0])
        font_size = int(C.next_player_button[1])
        pygame.draw.rect(self.window, C.draw_button_color, button_rect, border_radius=12)
        font = pygame.font.SysFont(None, font_size)
        text = font.render("Next Player", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.window.blit(text, text_rect)


    def draw_tray_background(self):
        pygame.draw.rect(
            self.window,
            (69, 69, 69), 
            (C.tray_background_x, C.tray_background_y , C.tray_background_width ,  C.tray_background_height ),
            border_radius=20)
        

    def draw_tray_grid(self): 
        for (row, col), (x, y) in C.tray_slot_coordinates.items():
            item_in_slot = self.chip_tracker.tray_grid.slots[(row, col)]
            if item_in_slot is None:
                self.draw_empty_slot(x, y)
            elif isinstance(item_in_slot, Chip):
                self.draw_chip(item_in_slot, x, y)
    
    
    def draw_undo_all_confirmation(self):
        if self.player_interaction.warning_window == True:
            width, height = 400, 200
            x = (C.window_width - width) // 2
            y = (C.window_height - height) // 2
            pygame.draw.rect(self.window, (240, 240, 240), (x, y, width, height), border_radius=15)
            pygame.draw.rect(self.window, (0, 0, 0), (x, y, width, height), 3, border_radius=15)

            # Text
            font = pygame.font.SysFont(None, 24)
            text = font.render("Are you sure you want to undo all the moves?", True, (0, 0, 0))
            self.window.blit(text, (x + 20, y + 40))

            # Yes button (green)
            yes_rect = pygame.Rect(x + 50, y + 120, 100, 40)
            pygame.draw.rect(self.window, (0, 200, 0), yes_rect, border_radius=10)
            yes_text = font.render("Yes", True, (255, 255, 255))
            self.window.blit(yes_text, (yes_rect.x + 25, yes_rect.y + 5))

            # No button (red)
            no_rect = pygame.Rect(x + 250, y + 120, 100, 40)
            pygame.draw.rect(self.window, (200, 0, 0), no_rect, border_radius=10)
            no_text = font.render("No", True, (255, 255, 255))
            self.window.blit(no_text, (no_rect.x + 30, no_rect.y + 5))

            # Save button rects for click detection
            self.undo_all_yes_rect = yes_rect
            self.undo_all_no_rect = no_rect
                





        








