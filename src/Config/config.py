import os
import pygame
class C:
    '''CONFIGURATION VARIABLES'''

    '''Board'''
    board_rows = 5
    board_cols = 29
    tray_rows = 5
    tray_cols = 16
    tray_visible_rows = 2

    board_horizontal_edge = 15 # border edge of the slots, left and right
    board_vertical_edge = 20  # border edge of the slots, top and bottom

    slot_horizontal_spacing = 5   # spacing between chips
    slot_vertical_spacing = 50   # spacing between chips


    '''Tray'''
    tray_background_extra_width = 60   #adds extra width to the tray background
    tray_background_extra_height = 20   #adds extra height to the tray background

    tray_space_from_bottom_of_the_screen = 20

    tray_slot_vertical_spacing = 5
    tray_slot_horizontal_spacing = 5

    
    '''Buttons on the right'''
    side_rectangle_space_from_tray = 10
    side_rectangle_space_from_window = 10

    side_rectangle_horizontal_space_between_buttons = 20
    side_rectangle_vertical_space_between_buttons = 20
    side_rectangle_horizontal_space_from_button_to_tray = 40
    side_rectangle_vertical_space_from_button_to_tray = 20


    

    '''Draw Button'''
    draw_button_color = (69, 69, 69) 


    '''Sort Tray Button'''
    sort_tray_button_color = (69, 69, 69) 

    '''Undo Move Button'''
    undo_button_color = (69, 69, 69) 

    '''Undo All Moves'''
    undo_all_moves_button_color = (69, 69, 69) 
    undo_cofirmation_button = None
    

    '''STATIC VARIABLES'''

    '''Window'''
    window = None
    window_width = None
    window_height = None

    '''Chip'''
    chip_width = None
    chip_height = None
    chip_sufrace = None
    FONT_PATH = os.path.join(os.path.dirname(__file__), '../../assets/fonts/Ubuntu-B.ttf')
    

    '''Slot Coordinates'''
    board_slot_coordinates = None
    tray_slot_coordinates = None

    '''Tray'''
    tray_grid_width = None
    tray_grid_height = None
    tray_grid_x = None
    tray_grid_y = None
    tray_background_width = None
    tray_background_height = None
    tray_background_x = None
    tray_background_y = None
    tray_background = None

    tray_up_button = None
    tray_down_button = None

    '''Undo all moves waring window'''
    undo_all_white_rect = None
    undo_all_black_rect = None
    undo_all_main_text_fontsize =None
    undo_all_yes_rect = None
    undo_all_no_rect = None
    undo_all_yes_text_size = None

    '''Buttons To The Right Ratio'''
    right_rect = None


    '''Buttons To The Right Coordinates'''
    right_buttons = {}
    right_buttons_font_size = {}


    '''Next Player Button'''
    next_player_button = None

    error_message_coord = None
    error_message_rect = None
    error_message_behind = None
    next_player_ready_button = None
    current_player_xy = None
    current_player_background_w = None
    current_player_background_b = None

    @staticmethod
    def setup_config():

        pygame.init()
        info = pygame.display.Info()

        # C.window = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)

        # for testing to see the terminal
        C.window = pygame.display.set_mode((1600, 800), pygame.RESIZABLE)

        C.window_width = C.window.get_width()
        C.window_height = C.window.get_height()


        C.setup_chip_dimentions()

        C.setup_tray()

        C.setup_right_rectangle()
        
        C.setup_right_buttons()

        C.setup_slot_coordinates()

        C.setup_next_player_button()

        C.set_up_confirmation_button()

        C.setup_error_message_coord()

        C.setup_undo_all_moves_confirmation()

        C.setup_next_player_ready_button()
      
        C.setup_tray_up_and_down_buttons()

        C.setup_current_player_display()
    @staticmethod
    def setup_current_player_display():
        x = C.tray_background_x + C.tray_background_width - C.chip_width * 3
        y = C.board_slot_coordinates[(C.board_rows-1,0)][1] + C.chip_height + C.board_vertical_edge //2 + 5
        C.current_player_background_b = (x-6, y-6,  C.chip_width *2 + 22, C.board_vertical_edge + 15)
        C.current_player_background_w = (x-7, y-7, C.chip_width *2 + 24, C.board_vertical_edge + 17)
        C.current_player_xy = (x, y)

    @staticmethod
    def setup_next_player_ready_button():
        button_width = int(C.window_width * 0.4)
        button_height = int(C.window_height * 0.15)
        button_x = (C.window_width - button_width) // 2
        button_y = (C.window_height - button_height) // 3
        C.next_player_ready_button = (button_x, button_y, button_width, button_height)
    
    @staticmethod
    def setup_error_message_coord():
        x =  C.next_player_button[0][0] //3
        y = C.board_slot_coordinates[(C.board_rows-1,0)][1] + C.chip_height + C.board_vertical_edge //2 + 5
        C.error_message_coord = (x,y)

        x = C.next_player_button[0][0] //4
        y = C.board_slot_coordinates[(C.board_rows-1,0)][1] + C.chip_height + C.board_vertical_edge // 4
        width = C.chip_width * 13
        height = C.board_vertical_edge * 2
        C.error_message_rect = (x, y, width, height)
        C.error_message_behind = (x-2, y-2, width+ 4, height+4)

    @staticmethod
    def setup_tray_up_and_down_buttons():
        arrow_width = 35
        arrow_height = 30
        x = C.tray_background_x + C.tray_background_width - C.tray_background_extra_width + 10
        y_up = C.tray_grid_y + int(C.chip_height *0.5 - arrow_height // 2) 
        y_down =  C.tray_grid_y + int(C.chip_height *1.5 - arrow_height // 2) 
        C.tray_down_button = (x, y_down, arrow_width, arrow_height)
        C.tray_up_button = (x, y_up, arrow_width, arrow_height)
   
    @staticmethod 
    def setup_next_player_button():
        width = C.tray_background_x // 2
        height = width // 3
        x = width // 2
        y = (C.window_height + C.tray_background_y) // 2 - (height // 2)

        rect = (x, y, width, height)
        font_size = int(rect[2] )   
        font = pygame.font.SysFont(None, font_size)
        text = font.render('Next Player', True, (255, 255, 255))
        text_rect = text.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
        while text_rect.width > rect[2] * 0.8 and font_size > 10:
            font_size -= 1
            font = pygame.font.SysFont(None, font_size)
            text = font.render("Next Player", True, (255, 255, 255))
            text_rect = text.get_rect(center=(rect[0] + rect[2] //2 , rect[1] + rect[3] // 2))
            
        C.next_player_button = (rect, font_size)

    @staticmethod
    def setup_slot_coordinates():
        C.board_slot_coordinates = {}

        start_x = C.board_horizontal_edge + C.slot_horizontal_spacing / 2
        for row in range(C.board_rows):
            for col in range(C.board_cols):
                x = start_x + (C.chip_width + C.slot_horizontal_spacing) * col
                y = C.board_vertical_edge +  (C.chip_height + C.slot_vertical_spacing) * row
                C.board_slot_coordinates[(row, col)] = (x, y)
                
        C.tray_slot_coordinates = {}
        for row in range(C.tray_rows):
            for col in range(C.tray_cols):
                x = C.tray_grid_x + col * (C.chip_width + C.tray_slot_horizontal_spacing)
                y = C.tray_grid_y + row * (C.chip_height + C.tray_slot_vertical_spacing) 
                C.tray_slot_coordinates[(row, col)] = (x, y)
               

    @staticmethod
    def set_up_confirmation_button():
        width = C.window_width // 3
        height = C.window_height // 3
        x = (C.window_width - width) // 2
        y = (C.window_height - height) // 2
        C.undo_cofirmation_button = (x  + 50, y + int(height* 0.8) , 100, 40)
    
    @staticmethod
    def setup_right_rectangle():
        # Position rectangle to the right of the tray background
        x = C.tray_background_x + C.tray_background_width + C.side_rectangle_space_from_tray  
        y = C.tray_background_y
        width = C.window_width - x - C.side_rectangle_space_from_window
        height = C.tray_background_height
        C.right_rect = (x, y, width, height)

    @staticmethod 
    def calculate_font_size(str_text: str, button_width: int, button_height: int):
        font_size = int(button_height)   
        font = pygame.font.SysFont(None, font_size)
        text = font.render(str_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(button_width, button_width))
        while text_rect.width > button_width * 0.8 and font_size > 10:
            font_size -= 1
            font = pygame.font.SysFont(None, font_size)
            text = font.render(str_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=(button_width, button_width))

        return font_size

    @staticmethod
    def setup_undo_all_moves_confirmation():
        width = C.window_width // 3
        height = C.window_height // 3
        x = (C.window_width - width) // 2
        y = (C.window_height - height) // 2
        C.undo_all_white_rect = (x, y, width, height)
        C.undo_all_black_rect = (x, y, width, height)
        C.undo_all_main_text_fontsize = C.calculate_font_size("Are you sure you want to undo all the moves?",width, height )

        button_width = int(width * 0.28)
        button_height = int(height * 0.18)
        button_y = y + int(height * 0.65)

        # Yes button (left side)
        yes_x = x + int(width * 0.12)
        C.undo_all_yes_rect = (yes_x, button_y, button_width, button_height)
        C.undo_all_yes_text_size = C.calculate_font_size("Yes", button_width, button_height)

    # No button (right side)
        no_x = x + width - int(width * 0.12) - button_width
        C.undo_all_no_rect = (no_x, button_y, button_width, button_height)
        
    @staticmethod
    def setup_right_buttons():

        button_rows = 2
        button_cols = 2
        # button_count = button_rows * button_cols
        button_margin_x = 15  # horizontal margin between buttons
        button_margin_y = 15  # vertical margin between buttons

        # Calculate button width and height
        button_width = (C.right_rect[2] - (button_cols + 1) * button_margin_x) // button_cols
        button_height = (C.right_rect[3] - (button_rows + 1) * button_margin_y) // button_rows
        button_names = ['Draw Chip', 'Undo Move', 'Sort Chips', 'Undo All Moves']

        name_index = 0
        for row in range(button_rows):
            for col in range(button_cols):
                x = C.right_rect[0] + button_margin_x + col * (button_width + button_margin_x)
                y = C.right_rect[1] + button_margin_y + row * (button_height + button_margin_y)
                C.right_buttons[button_names[name_index]] = (x, y, button_width, button_height)
                
                rect = (x, y, button_width, button_height)
                font_size = int(rect[2] )   
                font = pygame.font.SysFont(None, font_size)
                text = font.render(button_names[name_index], True, (255, 255, 255))
                text_rect = text.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
                while text_rect.width > rect[2] * 0.8 and font_size > 10:
                    font_size -= 1
                    font = pygame.font.SysFont(None, font_size)
                    text = font.render(button_names[name_index], True, (255, 255, 255))
                    text_rect = text.get_rect(center=(rect[0] + rect[2] //2 , rect[1] + rect[3] // 2))
                C.right_buttons_font_size[button_names[name_index]] = font_size
                name_index += 1

    @staticmethod
    def setup_chip_dimentions():
        C.chip_width = int(((C.window_width - C.board_horizontal_edge * 2) - C.slot_horizontal_spacing * (C.board_cols - 1)) / C.board_cols) 
        C.chip_height = int((((C.window_height - C.board_vertical_edge * 2) - C.tray_background_extra_height * 2 ) - C.slot_vertical_spacing * C.board_rows)  / (C.board_rows + C.tray_visible_rows))
        C.chip_sufrace = pygame.Surface((C.chip_width, C.chip_height))

    @staticmethod
    def setup_tray():
        C.tray_grid_width = (C.chip_width * C.tray_cols) + C.tray_slot_horizontal_spacing * (C.tray_cols - 1) 
        C.tray_grid_height = (C.chip_height * C.tray_visible_rows) + C.tray_slot_vertical_spacing * (C.tray_visible_rows - 1)
        C.tray_background_width = C.tray_grid_width + (C.tray_background_extra_width * 2)
        C.tray_background_height = C.tray_grid_height + (C.tray_background_extra_height * 2)

        C.tray_grid_x = int(C.window_width * 0.5 -  C.tray_grid_width / 2) 
        C.tray_grid_y = int(C.window_height - C.tray_space_from_bottom_of_the_screen) - C.tray_background_extra_height - C.tray_grid_height
        C.tray_background_x =  int(C.window_width * 0.5 - C.tray_background_width / 2)
        C.tray_background_y = C.tray_grid_y - C.tray_background_extra_height 
        C.tray_background = (C.tray_background_x , C.tray_background_y, C.tray_background_width, C.tray_background_height)
