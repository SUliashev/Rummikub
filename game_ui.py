import pygame
from chip import Chip
from chip_validator import ChipValidator
from chip_tracker import ChipTracker  # Import the ChipTracker class
from tray_grid import TrayGrid
from config import Config

class GameUI:
    def __init__(self, chip_tracker, chip_validator, current_player):
        self.window = Config.window 
        print('size', self.window.get_size())
        pygame.display.set_caption("Rummikub")
        self.chip_tracker = chip_tracker  # Use ChipTracker for chip management
        self.chip_validator = chip_validator
        self.current_player = current_player


    def draw(self):
        """
        Draw the board and chips.
        """
        self.window.fill((39,105,127))  # Clear the screen
        
        # self.draw_board_grid()
        self.draw_tray_background()
        self.draw_tray_grid()
        self.draw_hovering_slot()
        self.draw_moving_chip()
        self.draw_draw_chip_button()
        self.draw_next_player_button()
        self.draw_board_slots()
        self.draw_incorrect_chip_combination()
        # self.show_hovering_slot()
        # self.show_hovering_tray_slot()
        

    # def draw_empty_slot(self, x, y):
    #     border_radius = 9 
    #     rect = pygame.draw.rect(
    #             self.window, (255, 255, 255),
    #             (x, y, Config.chip_width, Config.chip_height),
    #             2, border_radius=border_radius
    #         )
    #     return rect           # not sure about this return 
    
    def draw_chip(self, chip, x, y):
        chip_drawing = self.window.blit(chip.sprite, (x, y))

        return chip_drawing
    
    def draw_board_slots(self):
        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            x , y = self.chip_tracker.board_grid.slot_coordinates[row, col]
            if item_in_slot is None:
                if self.chip_tracker.dragging_chip.chip == None :
                    self.draw_empty_slot(x, y)
                else:
                    validation_slot = self.chip_validator.slots.get((row, col), None)
                    if validation_slot == False:
                        self.draw_validation_slot(x, y, False)
                    elif validation_slot == True:
                        self.draw_validation_slot(x, y, True)
                    else:
                        self.draw_empty_slot(x, y)
            else:
                self.draw_chip(item_in_slot, x, y)

    def draw_empty_slot(self, x: int, y: int):
            border_radius = 9
            thickness = 2
            pygame.draw.rect(
            self.window, (255, 255, 255),
            (x, y, Config.chip_width, Config.chip_height),
            thickness, border_radius=border_radius
        )
    
    def draw_validation_slot(self, x: int, y: int, correct: bool):
        if correct:
            color =(0, 255, 0)
        else:
            color = (255, 0, 0)
        border_radius = 9
        rect = pygame.draw.rect(
                self.window, color,
                (x, y, Config.chip_width, Config.chip_height),
                2, border_radius=border_radius
            )



    def draw_incorrect_chip_combination(self):
        for (row, col), correct in self.chip_validator.slots_on_board.items():
            if not correct:
                self.draw_invalid_placed_chip_border(*self.chip_tracker.board_grid.slot_coordinates[row, col])
                
    def draw_invalid_placed_chip_border(self, x, y):       # can improve on this a little
        thickness = 5
        border_radius = 15
        pygame.draw.rect(
        self.window, (255, 0, 0),
        (x - thickness , y - thickness , Config.chip_width + thickness * 2, Config.chip_height  + thickness * 2),
        thickness, border_radius=border_radius
    )
        

        
    def draw_slot_validation(self): #all slots are shown for the testing stage

        for (row, col), chip in self.chip_tracker.board_grid.slots.items():
            if chip == None:
                self.draw_validation_slot(row, col)
            else: 
                (x, y) = self.chip_tracker.board_grid.slot_coordinates[row, col]
                self.draw_chip(chip, x, y)




    def draw_board_grid(self):
        if self.chip_tracker.dragging_chip.chip == None:
            self.draw_empty_slots()
            
        else:
            self.draw_slot_validation()

        font = pygame.font.SysFont(None, 18)  # Small font for column numbers
        for (row, col), (x, y) in self.chip_tracker.board_grid.slot_coordinates.items():
                col_text = font.render(str(col + 1), True, (200, 200, 0))
                self.window.blit(col_text, (x + 4, y + 2))


    def draw_moving_chip(self):
        if self.chip_tracker.dragging_chip.chip:
            chip = self.chip_tracker.dragging_chip.chip
            mouse_x, mouse_y = pygame.mouse.get_pos()
            chip.x = mouse_x - Config.chip_width / 2
            chip.y = mouse_y - Config.chip_height / 2
            self.draw_chip(chip, chip.x, chip.y)
    
    def draw_draw_chip_button(self):
        button_rect = pygame.Rect(Config.draw_button_x, Config.draw_button_y, Config.draw_button_width ,  Config.draw_button_height )
        font_size = int(Config.draw_button_width * 0.2)
        pygame.draw.rect(self.window, Config.draw_button_color, button_rect, border_radius=12)
        font = pygame.font.SysFont(None, font_size)
        text = font.render("Draw Chip", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.window.blit(text, text_rect)
    
    def draw_next_player_button(self): #to update later with config data
        button_rect = pygame.Rect(Config.next_player_button_x, Config.next_player_button_y, Config.draw_button_width ,  Config.draw_button_height )
        font_size = int(Config.draw_button_width * 0.2)
        pygame.draw.rect(self.window, Config.draw_button_color, button_rect, border_radius=12)
        font = pygame.font.SysFont(None, font_size)
        text = font.render("Next Player", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.window.blit(text, text_rect)


    def draw_hovering_slot(self):
        coordinates = self.chip_tracker.hovering_slot
        if coordinates == None:
            return
        
        elif coordinates[0] == 'tray':
            x, y = self.chip_tracker.tray_grid.slot_coordinates[coordinates[1]]
        elif coordinates[0] == 'board':
            x, y = self.chip_tracker.board_grid.slot_coordinates[coordinates[1]]

        border_radius = 17
        rect = pygame.draw.rect(
                self.window, (0, 0, 255),
                (x, y, Config.chip_width, Config.chip_height),
                2, border_radius=border_radius
            )
        

    def draw_tray_background(self):
        pygame.draw.rect(
            self.window,
            (60, 60, 60),  # Tray background color, adjust as needed
            (Config.tray_background_x, Config.tray_background_y , Config.tray_background_width ,  Config.tray_background_height ),
            border_radius=20
        )

    def draw_tray_grid(self): 
        for (row, col), (x, y) in self.chip_tracker.tray_grid.slot_coordinates.items():
            item_in_slot = self.chip_tracker.tray_grid.slots[(row, col)]
            if item_in_slot is None:
                self.draw_empty_slot(x, y)
            elif isinstance(item_in_slot, Chip):
                self.draw_chip(item_in_slot, x, y)
    
    

       





    








