from src.Core.game_controller import GameController
from src.GameUI.sprite_generator import ChipSpriteGenerator
from src.Config.config import C
from src.Core.event_dispatcher import EventDispatcher
import pygame
import sys


def main(players):
    C.setup_config()
    dispatcher = EventDispatcher()
    chips_sprites = ChipSpriteGenerator.generate_all_chips()
    
    game_controller = GameController(chips_sprites, dispatcher, players)
    game_controller.run()


def select_number_of_players():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Select Number of Players")
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    selected = 2

    def draw_menu():
        screen.fill((30, 30, 30))
        title = font.render("Select Players", True, (200, 200, 0))
        screen.blit(title, (180, 40))
        for i in range(2, 5):
            color = (255, 255, 255) if selected == i else (100, 100, 100)
            text = font.render(f"{i} Player{'s' if i > 1 else ''}", True, color)
            screen.blit(text, (220, 80 + i * 60))
        pygame.display.flip()

    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = selected + 1 if selected < 4 else 2
                elif event.key == pygame.K_UP:
                    selected = selected - 1 if selected > 1 else 4
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                    return selected

        clock.tick(30)

if __name__ == "__main__":
    players = select_number_of_players()
    main(players)


