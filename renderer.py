import pygame
from images import images

def draw_everything(surface, objects):
    surface.fill((255, 255, 255))
    for obj in objects:
        if obj[0] == "clock":
            clock = pygame.font.Font(None, 32)
            surface.blit(clock.render(obj[1], 20, (0, 0, 0)), (obj[2], obj[3]))
        else:
            surface.blit(images[obj[0]], (obj[1], obj[2]))