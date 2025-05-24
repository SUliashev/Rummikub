import pygame
from game_controller import GameController

def main():
    pygame.init()
    window = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Rummikub")
    game_controller = GameController(window)
    game_controller.run()

if __name__ == "__main__":
    main()

