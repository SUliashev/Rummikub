class Config:


    window_width = None
    window_height = None

    relative_width = None
    relative_height = None

    chip_width = None
    chip_height = None

    '''Tray'''
    tray_grid_x = None
    tray_grid_y = None

    tray_background_extra_width = 150
    tray_background_extra_height = 15
    tray_background_width = None
    tray_background_height = None
    tray_background_x = None
    tray_background_y = None

    '''Draw Button'''
    draw_button_color = (144, 255, 0)  # Green
    draw_button_width = 250
    draw_button_height = 70
    draw_button_x = None
    draw_button_y = None

    board_rows = 5
    board_cols = 29
    tray_rows = 2
    tray_cols = 13

    slot_spacing = 2

    
    @staticmethod
    def setup_config():
        import pygame
        pygame.init()
        info = pygame.display.Info()

        REFERENCE_WIDTH = 1920
        REFERENCE_HEIGHT = 1080
        Config.window_width = info.current_w
        Config.window_height = info.current_h

        Config.relative_width = Config.window_width / REFERENCE_WIDTH
        Config.relative_height = Config.window_height / REFERENCE_HEIGHT

        Config.chip_width = int(Config.window_width / Config.board_cols) - Config.slot_spacing
        Config.chip_height = int(info.current_h * 0.083)

        Config.tray_background_width = (Config.chip_width + Config.slot_spacing) * Config.tray_cols
        Config.tray_background_height = Config.chip_height * Config.tray_rows 
        Config.tray_grid_x = int(info.current_w * 0.5 -  Config.tray_background_width / 2) 
        Config.tray_grid_y = int(info.current_h * 0.93 -  Config.tray_background_height )
        Config.tray_background_x =  Config.tray_grid_x - (Config.tray_background_extra_width // 2 * Config.relative_width)
        Config.tray_background_y = Config.tray_grid_y - (Config.tray_background_extra_height // 2 * Config.relative_height)
      

        Config.draw_button_x = int(info.current_w * 0.9 - Config.draw_button_width // 2) * Config.relative_width
        Config.draw_button_y = int(info.current_h * 0.9 - Config.draw_button_height - 20) * Config.relative_height
        