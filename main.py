from game_controller import GameController
from chip_sprite_generator import ChipSpriteGenerator
from config import Config

def main():
    Config.setup_config()

    chips_sprites = ChipSpriteGenerator.generate_all_chips()

    game_controller = GameController(chips_sprites)
    game_controller.run()


if __name__ == "__main__":
    main()

