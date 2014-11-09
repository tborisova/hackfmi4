import pygame
from images import images

def draw_everything(surface, objects):
    surface.fill((255, 255, 255))
    for obj in objects:
        if obj[0] == "clock":
            clock = pygame.font.Font(None, 32)
            surface.blit(clock.render(obj[1], 20, (0, 0, 0)), (obj[2], obj[3]))
        else:
            img = images[obj[0]]
            if len(obj) > 3:    
                rotated = pygame.transform.rotate(img, obj[3])
                size = rotated.get_size()
                subrect = img.get_rect()
                subrect.width = 84
                subrect.height = 83
                subrect.centerx = size[0] // 2
                subrect.centery = size[1] // 2
                newimg = rotated.subsurface(subrect)
                img = newimg
            print(obj[1], obj[2])
            surface.blit(img, (obj[1], obj[2]))