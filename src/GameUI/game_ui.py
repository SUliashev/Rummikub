import pygame
from src.Core.chip import Chip
from src.Config.config import Config

class GameUI:
    def __init__(self, chip_tracker, chip_validator, current_player, dispatcher):
        self.window = Config.window 
        print('size', self.window.get_size())
        pygame.display.set_caption("Rummikub")
        self.chip_tracker = chip_tracker  # Use ChipTracker for chip management
        self.chip_validator = chip_validator
        self.current_player = current_player


    def draw(self):
        self.window.fill((39,105,127))  # Clear the screen

        self.draw_tray_background()
        self.draw_tray_grid()

        self.draw_next_player_button()

        self.draw_board_slots()

        self.draw_incorrect_chip_combination()      # shows which combinations on the board are not valid
        self.draw_hovering_slot()
        self.draw_moving_chip()
        self.draw_side_rectangle()
        self.draw_right_side_buttons()
        self.draw_selection_rectangle()
        self.show_selected_chips()
    
    def show_selected_chips(self):
        if self.chip_tracker.selected_chips:
            for slot, chip in self.chip_tracker.selected_chips:
                self.draw_chip_hue(*Config.tray_slot_coordinates[slot])

    def draw_selection_rectangle(self):
        if self.chip_tracker.draw_selection:
            x1, y1 = self.chip_tracker.selection_start
            x2 = self.chip_tracker.mouse_x
            y2 = self.chip_tracker.mouse_y
            rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            # Draw a semi-transparent fill
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill((0, 120, 255, 60))  # RGBA: blue with alpha
            self.window.blit(s, rect.topleft)
            # Draw the border
            pygame.draw.rect(self.window, (0, 120, 255), rect, 2)

        
    def draw_side_rectangle(self):
        pygame.draw.rect(
            self.window,
            (200, 200, 200),  # Rectangle color
            (Config.right_rect),
            border_radius=12
        )

    def draw_right_side_buttons(self):
        for button_name, rect in Config.right_buttons.items():
            pygame.draw.rect(
                self.window,
                (69, 69, 69),  # Button color
                rect,
                border_radius=8
        )
            font_size = Config.right_buttons_font_size[button_name]
            font = pygame.font.SysFont(None, font_size)
            text = font.render(button_name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))


            self.window.blit(text, text_rect)



    def draw_board_slots(self):
        draw_validation_for_all_slots = False   # testing variable, if False, it only shows the validation for the slots that are located next to chips
        draw_numbers_next_to_slots = True       # testing stage, adds numbers next to the slots on the board
        font = pygame.font.SysFont(None, 18)

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            x , y = Config.board_slot_coordinates[row, col]
            if item_in_slot is None:
                if self.chip_tracker.dragging_chip.chips == None :
                    self.draw_empty_slot(x, y)
                else:
                    if draw_validation_for_all_slots:
                        validation_slot = self.chip_validator.slots.get((row, col), None)
                        if validation_slot == False:
                            self.draw_validation_slot(x, y, False)
                        else: 
                            self.draw_validation_slot(x, y, True)
                    else:           # Code for when draw_validation_for_all_slots is False
                        if not self.chip_validator.slot_next_to_chip[(row, col)]:
                            self.draw_empty_slot(x, y)
                            if draw_numbers_next_to_slots:
                                col_text = font.render(str(col + 1), True, (200, 200, 0))
                                self.window.blit(col_text, (x + 4, y + 2))
                            continue
                        validation_slot = self.chip_validator.slots[(row, col)]
                        if validation_slot == False:
                            self.draw_validation_slot(x, y, False)
                        else: 
                            self.draw_validation_slot(x, y, True)
               
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
        (x, y, Config.chip_width, Config.chip_height),
        thickness, border_radius=border_radius)
        
    
    def draw_validation_slot(self, x: int, y: int, correct: bool):
        if correct:
            color =(0, 255, 0)
        else:
            color = (255, 0, 0)
        border_radius = 9
        pygame.draw.rect(
            self.window, color,
            (x, y, Config.chip_width, Config.chip_height),
            2, border_radius=border_radius)
            
        
    def draw_hovering_slot(self):
        if not self.chip_tracker.hovering_slot:
            return
        
        slot_type, slot = self.chip_tracker.hovering_slot       
        if slot_type == 'tray':
            x, y = Config.tray_slot_coordinates[slot]
        elif slot_type == 'board':
            x, y = Config.board_slot_coordinates[slot]

        border_radius = 9
        rect = pygame.draw.rect(
                self.window, (0, 30, 140),
                (x, y, Config.chip_width, Config.chip_height),
                3, border_radius=border_radius)
            
        
    def draw_incorrect_chip_combination(self):
        for (row, col), correct in self.chip_validator.slots_on_board.items():
            if not correct:
                self.draw_invalid_placed_chip_border(*Config.board_slot_coordinates[row, col])
                

    def draw_invalid_placed_chip_border(self, x, y):       
        thickness = 5
        border_radius = 15
        pygame.draw.rect(
        self.window, (255, 0, 0),
        (x - thickness , y - thickness , Config.chip_width + thickness * 2, Config.chip_height  + thickness * 2),
        thickness, border_radius=border_radius)
        
            
    def draw_chip_hue(self, x, y, width=None, height=None, outline_thickness=10, border_radius=10):
        """
        Draws a white, semi-transparent hue (outline) behind a chip at (x, y).
        """
        if width is None:
            width = Config.chip_width
        if height is None:
            height = Config.chip_height

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
        if self.chip_tracker.dragging_chip.chips:
            chip = self.chip_tracker.dragging_chip.chips
            x = self.chip_tracker.mouse_x - Config.chip_width / 2
            y = self.chip_tracker.mouse_y - Config.chip_height / 2

            # Draw the hue behind the chip
            self.draw_chip_hue(x, y)

            # Draw the chip itself
            self.draw_chip(chip, x, y)
        
    def draw_next_player_button(self): #to update later with config data
        button_rect = pygame.Rect(Config.next_player_button[0])
        font_size = int(Config.next_player_button[1])
        pygame.draw.rect(self.window, Config.draw_button_color, button_rect, border_radius=12)
        font = pygame.font.SysFont(None, font_size)
        text = font.render("Next Player", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.window.blit(text, text_rect)


    def draw_tray_background(self):
        pygame.draw.rect(
            self.window,
            (69, 69, 69), 
            (Config.tray_background_x, Config.tray_background_y , Config.tray_background_width ,  Config.tray_background_height ),
            border_radius=20)
        

    def draw_tray_grid(self): 
        for (row, col), (x, y) in Config.tray_slot_coordinates.items():
            item_in_slot = self.chip_tracker.tray_grid.slots[(row, col)]
            if item_in_slot is None:
                self.draw_empty_slot(x, y)
            elif isinstance(item_in_slot, Chip):
                self.draw_chip(item_in_slot, x, y)
    
    

        





        








