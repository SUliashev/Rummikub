import pygame
from game_controller import GameController
from chip_sprite_generator import ChipSpriteGenerator
from config import Config

def main():
    setup_config()
    
    # Generate chips after knowing the window size

    chips_sprites = ChipSpriteGenerator.generate_all_chips()

    game_controller = GameController(chips_sprites)
    game_controller.run()

def setup_config():
    pygame.init()
    info = pygame.display.Info()
    Config.window_width = info.current_w
    Config.window_height = info.current_h
    Config.chip_width = int(info.current_w * ((1920 // Config.board_cols) / 1920) - Config.slot_spacing)
    Config.chip_height = int(info.current_h * 0.083)
    Config.tray_background_width = (Config.chip_width + Config.slot_spacing) * Config.tray_cols  
    Config.tray_background_height = Config.chip_height * Config.tray_rows + (Config.tray_rows - 1)
    Config.tray_grid_x = int(info.current_w * 0.5 -  Config.tray_background_width / 2)
    Config.tray_grid_y = int(info.current_h * 0.93 -  Config.tray_background_height )
    Config.tray_background_x =  Config.tray_grid_x - Config.tray_background_extra_width // 2
    Config.tray_background_y = Config.tray_grid_y - Config.tray_background_extra_height // 2


if __name__ == "__main__":
    main()

