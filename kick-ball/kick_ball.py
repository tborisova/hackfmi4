from pygame.locals import *
import pygame

from setup import *


class Ball(pygame.sprite.Sprite):

    """ The ball """

    def __init__(self, image_name='player.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(IMAGES_PATH + image_name)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(image)
        self.gravity = GRAVITY
        self.cap = CAP
        self.bounce = BOUNCE
        self.friction = FRICTION
        self.kick = KICK
        self.x = self.rect.x
        self.y = self.rect.y
        self.dx = 0
        self.dy = 0
        self.on_ground = False
        self.spin = 0
        self.angle = 0

    def center(self):
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        self.x += self.dx / 2
        self.y += self.dy / 2
        self.angle += self.spin
        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360
        if not self.on_ground:
            self.dy += self.gravity
        if self.dy > self.cap:
            self.dy = self.cap
        if self.on_ground:
            self.dx *= self.friction
            self.spin = -self.dx
        if self.on_ground and abs(self.dx) - 0.5 < 0:
            self.dx = 0
            self.spin = -self.dx
        self.rect.x = self.x
        self.rect.y = self.y
