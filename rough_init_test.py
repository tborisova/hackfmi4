import pygame
import renderer
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))


    
while True:
    renderer.draw_everything(screen, (("top_wall", 50, 50),) )

    pygame.display.update()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
