import pygame
from images import images

def draw_everything(surface, objects):
    for obj in objects:
        print(obj[0])
        surface.blit(images[obj[0]], (obj[1], obj[2]))