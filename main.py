import pygame
from board import Board
from chip import Chip

pygame.init()
window = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

board = Board()
chip = Chip(500, 700)




for keys, value in board.row2.items():
    print(f"key: {keys}, values: {value}")

while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            exit()


    window.fill((0,0,0))
    # board.draw_lines()
    chip.draw(board.window)

    
    pygame.display.flip()

    clock.tick(60)

