import pygame
from images import images

def draw_everything(surface, objects):
    surface.fill((255, 255, 255))
    for obj in objects:
        surface.blit(images[obj[0]], (obj[1], obj[2]))