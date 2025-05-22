import pygame
from chip import Chip


pygame.init()
window = pygame.display.set_mode((1920, 1080))


window.fill((0,0,0))
chip = pygame.image.load("test_chip.png")

chip = {}
chip[0] = Chip(0, 0)
window.blit(chip[0].sprite, (chip[0].x , chip[0].y))
for i in range(1, 21):
    next_to = i % 3 != 0
    if next_to:
        step = 1
    else:
        step = 2
    chip[i] = Chip(chip[i-1].x + chip[i-1].width*step, 0)
    window.blit(chip[i].sprite, (chip[i].x , chip[i].y))

chip[21] = Chip(0,  chip[1].height * 2)
window.blit(chip[21].sprite, (chip[21].x , chip[21].y))
for i in range(22, 25):
    chip[i] = Chip(0, chip[i-1].y + chip[i-1].height * 2)
    window.blit(chip[i].sprite, (chip[i].x , chip[i].y))

    
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
