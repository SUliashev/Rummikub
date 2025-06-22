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
    right_buttons_width = None
    right_buttons_height = None


    '''Buttons To The Right Coordinates'''
    right_buttons = None
    draw_button_x = None
    draw_button_y = None
    sort_tray_button_x = None
    sort_tray_button_y = None
    undo_move_button_x = None
    undo_move_button_y = None
    undo_all_moves_button_x = None
    undo_all_moves_button_y = None


    '''Next Player Button'''
    next_player_button_x = None
    next_player_button_y = None

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

      
        Config.right_buttons_width =  Config.tray_background_x // 2 * 0.8
        Config.right_buttons_height = Config.right_buttons_width // 3

        Config.draw_button_x = int(Config.window_width  - Config.tray_background_x) + Config.right_buttons_width // 2 * 0.1
        Config.draw_button_y = int((Config.window_height + Config.tray_background_y) // 2) - Config.right_buttons_height // 2
        
    

        Config.next_player_button_x = Config.window_width - Config.draw_button_x - Config.right_buttons_width
        Config.next_player_button_y = Config.draw_button_y

    @staticmethod
    def setup_right_rectangle():
        # Position rectangle to the right of the tray background
        Config.right_rect_x = Config.tray_background_x + Config.tray_background_width + Config.side_rectangle_space_from_tray  
        Config.right_rect_y = Config.tray_background_y
        Config.right_rect_width = Config.window_width - Config.right_rect_x - Config.side_rectangle_space_from_window
        Config.right_rect_height = Config.tray_background_height


    @staticmethod
    def setup_right_buttons():
        button_count = 4
        button_margin = 15  # vertical margin between buttons
        button_height = (Config.right_rect_height - (button_count + 1) * button_margin) // button_count
        button_width = Config.right_rect_width - 2 * button_margin

        Config.right_buttons = []
        for i in range(button_count):
            x = Config.right_rect_x + button_margin
            y = Config.right_rect_y + button_margin + i * (button_height + button_margin)
            Config.right_buttons.append((x, y, button_width, button_height))






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

