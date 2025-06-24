from src.Core.game_controller import GameController
from src.GameUI.sprite_generator import ChipSpriteGenerator
from src.Config.config import C
from src.Core.event_dispatcher import EventDispatcher

def main():
    C.setup_config()

    chips_sprites = ChipSpriteGenerator.generate_all_chips()
    dispatcher = EventDispatcher()
    game_controller = GameController(chips_sprites, dispatcher)
    game_controller.run()


if __name__ == "__main__":
    main()

