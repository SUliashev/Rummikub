import os
import pygame
class Config:
    '''CONFIGURATION VARIABLES'''

    '''Board'''
    board_rows = 5
    board_cols = 29
    tray_rows = 2
    tray_cols = 13

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

    right_buttons_width = 250
    right_buttons_height = 70

    

    '''Draw Button'''
    draw_button_color = (69, 69, 69) 


    '''Sort Tray Button'''
    sort_tray_button_color = (69, 69, 69) 

    '''Undo Move Button'''
    undo_button_color = (69, 69, 69) 

    '''Undo All Moves'''
    undo_all_moves_button_color = (69, 69, 69) 

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


    '''Buttons To The Right Ratio'''
    right_rect = None


    '''Buttons To The Right Coordinates'''
    right_buttons = {}
    right_buttons_font_size = {}


    '''Next Player Button'''
    next_player_button = None

    @staticmethod
    def setup_config():

        pygame.init()
        info = pygame.display.Info()
        Config.window = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)

        Config.window_width = Config.window.get_width()
        Config.window_height = Config.window.get_height()
        
        Config.setup_chip_dimentions()

        Config.setup_tray()

        Config.setup_right_rectangle()
        
        Config.setup_right_buttons()

        Config.setup_slot_coordinates()

        Config.setup_next_player_button()
      
        Config.right_buttons_width =  Config.tray_background_x // 2 * 0.8
        Config.right_buttons_height = Config.right_buttons_width // 3

    

    @staticmethod 
    def setup_next_player_button():
        width = Config.tray_background_x // 2
        height = width // 3
        x = width // 2
        y = (Config.window_height + Config.tray_background_y) // 2 - (height // 2)

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
            
        Config.next_player_button = (rect, font_size)

    @staticmethod
    def setup_slot_coordinates():
        Config.board_slot_coordinates = {}

        start_x = Config.board_horizontal_edge + Config.slot_horizontal_spacing / 2
        for row in range(Config.board_rows):
            for col in range(Config.board_cols):
                x = start_x + (Config.chip_width + Config.slot_horizontal_spacing) * col
                y = Config.board_vertical_edge +  (Config.chip_height + Config.slot_vertical_spacing) * row
                Config.board_slot_coordinates[(row, col)] = (x, y)
                
        Config.tray_slot_coordinates = {}
        for row in range(Config.tray_rows):
            for col in range(Config.tray_cols):
                x = Config.tray_grid_x + col * (Config.chip_width + Config.tray_slot_horizontal_spacing)
                y = Config.tray_grid_y + row * (Config.chip_height + Config.tray_slot_vertical_spacing) 
                Config.tray_slot_coordinates[(row, col)] = (x, y)
               


    @staticmethod
    def setup_right_rectangle():
        # Position rectangle to the right of the tray background
        x = Config.tray_background_x + Config.tray_background_width + Config.side_rectangle_space_from_tray  
        y = Config.tray_background_y
        width = Config.window_width - x - Config.side_rectangle_space_from_window
        height = Config.tray_background_height
        Config.right_rect = (x, y, width, height)
        print('calculated')

    @staticmethod
    def setup_right_buttons():

        button_rows = 2
        button_cols = 2
        # button_count = button_rows * button_cols
        button_margin_x = 15  # horizontal margin between buttons
        button_margin_y = 15  # vertical margin between buttons

        # Calculate button width and height
        button_width = (Config.right_rect[2] - (button_cols + 1) * button_margin_x) // button_cols
        button_height = (Config.right_rect[3] - (button_rows + 1) * button_margin_y) // button_rows
        button_names = ['Draw Chip', 'Undo Move', 'Sort Chips', 'Undo All Moves']

        name_index = 0
        for row in range(button_rows):
            for col in range(button_cols):
                x = Config.right_rect[0] + button_margin_x + col * (button_width + button_margin_x)
                y = Config.right_rect[1] + button_margin_y + row * (button_height + button_margin_y)
                Config.right_buttons[button_names[name_index]] = ((x, y, button_width, button_height))
                
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
                Config.right_buttons_font_size[button_names[name_index]] = font_size
                name_index += 1

    @staticmethod
    def setup_chip_dimentions():
        Config.chip_width = int(((Config.window_width - Config.board_horizontal_edge * 2) - Config.slot_horizontal_spacing * (Config.board_cols - 1)) / Config.board_cols) 
        Config.chip_height = int((((Config.window_height - Config.board_vertical_edge * 2) - Config.tray_background_extra_height * 2 ) - Config.slot_vertical_spacing * Config.board_rows)  / (Config.board_rows + Config.tray_rows))
        Config.chip_sufrace = pygame.Surface((Config.chip_width, Config.chip_height))

    @staticmethod
    def setup_tray():
        Config.tray_grid_width = (Config.chip_width * Config.tray_cols) + Config.tray_slot_horizontal_spacing * (Config.tray_cols - 1) 
        Config.tray_grid_height = (Config.chip_height * Config.tray_rows) + Config.tray_slot_vertical_spacing * (Config.tray_rows - 1)
        Config.tray_background_width = Config.tray_grid_width + (Config.tray_background_extra_width * 2)
        Config.tray_background_height = Config.tray_grid_height + (Config.tray_background_extra_height * 2)

        Config.tray_grid_x = int(Config.window_width * 0.5 -  Config.tray_grid_width / 2) 
        Config.tray_grid_y = int(Config.window_height - Config.tray_space_from_bottom_of_the_screen) - Config.tray_background_extra_height - Config.tray_grid_height
        Config.tray_background_x =  int(Config.window_width * 0.5 - Config.tray_background_width / 2)
        Config.tray_background_y = Config.tray_grid_y - Config.tray_background_extra_height 

