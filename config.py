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

    

    '''Draw Button'''
    draw_button_color = (144, 255, 0)  # Green
    draw_button_width = 250
    draw_button_height = 70



    '''STATIC VARIABLES'''
    '''Window'''
    window_width = None
    window_height = None

    # relative_width = None
    # relative_height = None

    '''Board'''
    board_slot_edge_x = None 
    board_slot_edge_y = None
    board_bottom_edge_y = None

    '''Chip'''
    chip_width = None
    chip_height = None

    '''Tray'''
    tray_grid_width = None
    tray_grid_height = None
    tray_grid_x = None
    tray_grid_y = None
    tray_background_width = None
    tray_background_height = None
    tray_background_x = None
    tray_background_y = None


    '''Draw Button'''
    draw_button_x = None
    draw_button_y = None

    window = None

    @staticmethod
    def setup_config():
        import pygame
        pygame.init()
        info = pygame.display.Info()
        Config.window = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
        # REFERENCE_WIDTH = 1920
        # REFERENCE_HEIGHT = 1011
        Config.window_width = Config.window.get_width()
        Config.window_height = Config.window.get_height()
        

        # Config.relative_width = Config.window_width / REFERENCE_WIDTH
        # Config.relative_height = Config.window_height / REFERENCE_HEIGHT

        # Config.board_slot_edge_x = int(Config.board_horizontal_edge * Config.relative_width)
        # Config.board_slot_edge_y = int(Config.board_vertical_edge * Config.relative_height)

        # Config.board_bottom_edge_y = Config.window_height - Config.tray_background_y - Config.board_slot_edge_y
        # Config.board_bottom_edge_y = Config.window_height - Config.tray_background_y - Config.board_slot_edge_y

        Config.chip_width = int(((Config.window_width - Config.board_horizontal_edge * 2) - Config.slot_horizontal_spacing * (Config.board_cols - 1)) / Config.board_cols) 
        Config.chip_height = int((((Config.window_height - Config.board_vertical_edge * 2) - Config.tray_background_extra_height * 2 ) - Config.slot_vertical_spacing * Config.board_rows)  / (Config.board_rows + Config.tray_rows))

        Config.tray_grid_width = (Config.chip_width * Config.tray_cols) + Config.tray_slot_horizontal_spacing * (Config.tray_cols - 1) 
        Config.tray_grid_height = (Config.chip_height * Config.tray_rows) + Config.tray_slot_vertical_spacing * (Config.tray_rows - 1)
        Config.tray_background_width = Config.tray_grid_width + (Config.tray_background_extra_width * 2)
        Config.tray_background_height = Config.tray_grid_height + (Config.tray_background_extra_height * 2)

        Config.tray_grid_x = int(Config.window_width * 0.5 -  Config.tray_grid_width / 2) 
        Config.tray_grid_y = int(Config.window_height - Config.tray_space_from_bottom_of_the_screen) - Config.tray_background_extra_height - Config.tray_grid_height
        Config.tray_background_x =  int(Config.window_width * 0.5 - Config.tray_background_width / 2)
        Config.tray_background_y = Config.tray_grid_y - Config.tray_background_extra_height 
      
        
        Config.draw_button_x = int(Config.window_width * 0.9 - Config.draw_button_width // 2)
        Config.draw_button_y = int((Config.window_height + Config.tray_background_extra_height) * 0.5 - Config.draw_button_height // 2) 
        